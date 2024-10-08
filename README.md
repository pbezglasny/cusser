[![PyPI](https://img.shields.io/pypi/v/cusser)](https://pypi.org/project/cusser/)
[![Python package](https://github.com/getcuia/cusser/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/cusser/actions/workflows/python-package.yml)
[![PyPI - License](https://img.shields.io/pypi/l/cusser)](https://github.com/getcuia/cusser/blob/main/LICENSE)

# [cusser](https://github.com/getcuia/cusser#readme) 🤬

## Fork of [cusser](https://github.com/getcuia/cusser#readme) with python 3.11 fix

<div align="center">
    <img class="hero" src="https://github.com/getcuia/cusser/raw/main/banner.jpg" alt="cusser" width="33%" />
</div>

> A curses wrapper that understands ANSI escape code sequences

cusser is a lightweight Python package for teaching
[curses](https://docs.python.org/3/library/curses.html) how to use
[ANSI escape code sequences](https://en.wikipedia.org/wiki/ANSI_escape_code). It
works by wrapping the curses standard window object and intercepting escape code
sequences.

## Features

- ♻️ Easily integrate with the
  [standard `curses` module](https://docs.python.org/3/library/curses.html)
- 🕹️ Use the same escape code sequences
  [as you would with Colorama](https://github.com/tartley/colorama#recognised-ansi-sequences)
- 🖍️ Only one dependency: [stransi](https://github.com/getcuia/stransi) (for
  actuallly parsing escape code sequences)
- 🐍 Python 3.8+

## Installation

```console
$ pip install cusser
```

## Usage

```python
In[1]:
import curses

In[2]:
from cusser import Cusser

In[3]:


def app(stdscr) -> None:
    ...: """Start a new application."""
    ...:
    if not isinstance(stdscr, Cusser):
        ...: stdscr = Cusser(stdscr)
    ...:
    ...: ultra_violet = (100, 83, 148)
    ...: x, y = 34, 12
    ...: stdscr.addstr(
        ...:         f"\033[2J\033[{x};{y}H"
    ...: "\033[1;32mHello "
    ...:         f"\033[;3;38;2;{';'.join(map(str, ultra_violet))}m"
    ...: "cusser"
    ...:         "\033[m 🤬!"
    ...:     )
    ...: stdscr.refresh()
    ...: stdscr.getch()
    ...:


In[4]: curses.wrapper(app)

```

![Screenshot](https://github.com/getcuia/cusser/raw/main/screenshot.png)

## Credits

[Photo](https://github.com/getcuia/cusser/raw/main/banner.jpg) by
[Gwendal Cottin](https://unsplash.com/@gwendal?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on
[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
