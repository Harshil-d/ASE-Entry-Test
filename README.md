# ASE-Entry-Test

## Task 1 – Dependency Checker (`main.py`)

Checks every pinned dependency (`package==version`) in a requirements file against PyPI and reports:

- whether the package/version exists on PyPI
- whether it is compatible with Python 3.11 (via its `requires_python`)
- which dependency has the highest minimum Python requirement

## Input
```txt
django==4.2
numpy==2.3.0
scipy==1.7.0
scikit-learn==1.4.0
fastapi-agent-router==0.3.1
matplotlib==3.99.0
six==1.16.0
requests==2.32.0
```
## Output
```log
[DEBUG] django==4.2                    checked | found     | min python: 3.8   | compatible: yes (>=3.8)
[DEBUG] numpy==2.3.0                   checked | found     | min python: 3.11  | compatible: yes (>=3.11)
[DEBUG] scipy==1.7.0                   checked | found     | min python: 3.7   | compatible: no (>=3.7,<3.10)
[DEBUG] scikit-learn==1.4.0            checked | found     | min python: 3.9   | compatible: yes (>=3.9)
[DEBUG] fastapi-agent-router==0.3.1    checked | not found | min python: -     | compatible: -
[DEBUG] matplotlib==3.99.0             checked | not found | min python: -     | compatible: -
[DEBUG] six==1.16.0                    checked | found     | min python: 2.7   | compatible: yes (>=2.7, !=3.0.*, !=3.1.*, !=3.2.*)
[DEBUG] requests==2.32.0               checked | found     | min python: 3.8   | compatible: yes (>=3.8)

Dependencies checked: 8
Not found on PyPI: 2
Incompatible with Python 3.11: 1
Highest requirement: numpy==2.3.0 (>=3.11)
```