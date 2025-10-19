

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

#### Adjust thinkorswim Desktop resolution
1. Find thinkorswim shortcut or executable and right click and go to Properties.
2. Go to compatibility tab and click on "Change High DPI Settings" at the bottom.
3. At the bottom section, called "High DPI scaling override", tick the box and select "Application". Click all OKs and close everything.
4. Now when you open Thinkorswim app, the letters might look tiny. To fix this issue Click Setup -> Application Settings -> General/Look and Feel -> Change Font size to Large to Very Large depending on your preference.

### References
- [Github - Python for Algorithmic Trading Cookbook](https://github.com/PacktPublishing/Python-for-Algorithmic-Trading-Cookbook)
- [day trading guide](https://www.warriortrading.com/day-trading/#toc16)
- [thinkorswim scan filters](https://toslc.thinkorswim.com/center/howToTos/thinkManual/Scan/Filters)
- [Setting filters](https://www.youtube.com/watch?v=KeewYEhY6MM)