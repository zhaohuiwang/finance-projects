

Disable `.pyc` File Generation:

Set the `PYTHONDONTWRITEBYTECODE` environment variable to prevent Python from creating `.pyc` files:
```bash 
export PYTHONDONTWRITEBYTECODE=1
```
Or set it in your script:
```python
pythonimport os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
```
Note: This slows down script execution slightly, as Python recompiles the source code each time.

Version Control: Use .gitignore to exclude `.pyc` and `__pycache__` from Git.


```bash
(finance) zhaohuiwang@WangFamily:/mnt/e/zhaohuiwang/dev/finance-projects$ uv run -m schwab_dev.src.scripts.get_tokens
```

Without `__init__.py`, I can still run the above command as a module. 