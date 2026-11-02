"""Check every pinned package in requirements.txt against PyPI:
1. does the package/version exist?
2. is it compatible with Python 3.11?
3. which dependency has the highest Python requirement?

Usage: python main.py [path/to/requirements.txt]
Needs: pip install packaging certifi
"""

import json
import ssl
import sys
import urllib.error
import urllib.request

from packaging.specifiers import SpecifierSet
from packaging.version import Version

PYTHON_VERSION = "3.11"

# Use certifi's CA bundle if available (fixes CERTIFICATE_VERIFY_FAILED on macOS)
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()


def get_requires_python(name, version):
    """Return the release's requires_python ("" if unset), or None if not on PyPI."""
    url = f"https://pypi.org/pypi/{name}/{version}/json"
    try:
        with urllib.request.urlopen(url, timeout=10, context=SSL_CONTEXT) as response:
            return json.load(response)["info"]["requires_python"] or ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except urllib.error.URLError as e:
        sys.exit(f"Cannot reach PyPI: {e.reason}")


def min_python(spec):
    """Lowest Python version allowed by a requires_python string, e.g. '>=3.12' -> 3.12."""
    lower_bounds = [Version(s.version) for s in SpecifierSet(spec) if s.operator in (">=", ">", "~=", "==")]
    return max(lower_bounds) if lower_bounds else None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"
    try:
        with open(path) as f:
            lines = [line.split("#")[0].strip() for line in f]
    except FileNotFoundError:
        sys.exit(f"File not found: {path}")

    checked = not_found = incompatible = 0
    highest = None  # (min python version, requirement, requires_python)

    for line in lines:
        if "==" not in line:
            continue
        name, version = [part.strip() for part in line.split("==", 1)]
        name = name.split("[")[0]  # drop extras like requests[socks]
        checked += 1

        spec = get_requires_python(name, version)
        if spec is None:
            not_found += 1
            continue

        if spec and PYTHON_VERSION not in SpecifierSet(spec):
            incompatible += 1

        minimum = min_python(spec) if spec else None
        if minimum and (highest is None or minimum > highest[0]):
            highest = (minimum, f"{name}=={version}", spec)

    print(f"Dependencies checked: {checked}")
    print(f"Not found on PyPI: {not_found}")
    print(f"Incompatible with Python {PYTHON_VERSION}: {incompatible}")
    if highest:
        print(f"Highest requirement: {highest[1]} ({highest[2]})")
    else:
        print("Highest requirement: none")


if __name__ == "__main__":
    main()
