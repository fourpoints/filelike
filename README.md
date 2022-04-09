# filelike
File-like objects for terminal and clipboard

```python
# File-like is one of pathlib.Path, filelike.Clipboard, filelike.Terminal
output = Path() / "file.txt"
output = Clipboard()
output = Terminal()


# Write to a file-like object
with output.open(mode="w", encoding="utf-8") as f:
    print("hello world", file=f)

# Read from a file-like object
with output.open(mode="r", encoding="utf-8") as f:
    print(f.read())
```
