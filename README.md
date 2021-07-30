# Overview

## Class

- `FlexlmLicenseManager` : a wrapper class to query license status to a license server

## Function

- `parse_query` : Parse query result and convert to a dictionary
- `get_license_status` : Query license status to a license server and get available number of licenses.

## Script

- `flexlmlic.py` : Print out the availbale number of licenses to stdout.

# Test

## Miniconda3

```powershell
(base) PS> conda create -n flexlmtools python=3.6
(base) PS> conda activate flexlmtools
(flexlmtools) PS> python -m pip install -e .[develop]
(flexlmtools) PS> pytest -v
```