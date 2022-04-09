from pathlib import Path
import tkinter as tk
import sys
import os


"""
|    | read | write | exists | inexists | truncate | append |   mode |
|----|------|-------|--------|----------|----------|--------|--------|
|  r |    X |       |     OK |    error |          |        |   text |
|  w |      |     X |     OK |   create |        X |        |   text |
|  a |      |     X |     OK |   create |          |      X |   text |
|  x |      |     X |  error |   create |          |        |   text |
|----|------|-------|--------|----------|----------|--------|--------|
|  + |    X |     X |      ? |        ? |        ? |      ? |      ? |
|  t |    ? |     ? |      ? |        ? |        ? |      ? |   text |
|  b |    ? |     ? |      ? |        ? |        ? |      ? | binary |

* truncate = clear file
* append = set seeker position at end
"""


class FileLike:
    _created = False
    _readable = False
    _writable = False
    _truncate = False
    _appending = False

    def __init__(self, mode, encoding, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.encoding = encoding

        # Copied from cpython/_pyio.FileIO
        # https://github.com/python/cpython/blob/677320348728ce058fa3579017e985af74a236d4/Lib/_pyio.py#L1491
        if 'x' in mode:
            self._created = True
            self._writable = True
        elif 'r' in mode:
            self._readable = True
        elif 'w' in mode:
            self._writable = True
            self._truncate = True
        elif 'a' in mode:
            self._appending = True

        if '+' in mode:
            self._readable = True
            self._writable = True

    def read(self):
        raise NotImplementedError

    def write(self, string):
        raise NotImplementedError


class ClipboardFile(FileLike, tk.Tk):
    def read(self):
        try:
            return self.clipboard_get()
        except tk.TclError:
            pass

    def write(self, string):
        print(f"'{string}' appended to clipboard")
        assert self._writable
        self.clipboard_append(string)

    def __enter__(self):
        if self._truncate:
            self.clipboard_clear()
        return self

    def __exit__(self, *exc):
        # if not self._readable and self._writable:
        self.mainloop()  # prevent clipboard from being cleared


class TerminalFile(FileLike):
    def read(self):
        return sys.stdin.readline()

    def write(self, string):
        assert self._writable
        sys.stdout.write(string)

    def __enter__(self):
        if self._truncate:
            os.system("cls")
        return self

    def __exit__(self, *exc):
        pass


class Clipboard:
    def open(self, mode=None, encoding=None):
        return ClipboardFile(mode, encoding)


class Terminal:
    def open(self, mode=None, encoding=None):
        return TerminalFile(mode, encoding)


if __name__ == "__main__":
    output = Path() / "file.txt"
    output = Clipboard()
    output = Terminal()


    with output.open(mode="w", encoding="utf-8") as f:
        print("hello world", file=f)

    with output.open(mode="r", encoding="utf-8") as f:
        print(f.read())
