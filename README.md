# Project Ripple <img align="right" width="150" height="150" src="https://github.com/Tejune/Project-Ripple/blob/master/project_ripple/images/arrow.png?raw=true">

Project Ripple is a lightweight 4-key rhythm player that runs using Quaver maps.

Created just for fun, don't expect many updates or anything of the sort.

## Dependencies
- [Quaver](https://store.steampowered.com/app/980610/Quaver/) installed (downloaded songs in the quaver folder are used by the player)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Python 3.11](https://www.python.org/downloads/release/python-3112/)

## Installing other dependencies and running
Run `run.pyw,` if this does not work you can manually install the project:
```
poetry install
poetry run ripple
```

## Installing globally
Requires a working [pipx](https://pypa.github.io/pipx/installation/) setup.
```
poetry build
pipx install .\dist\project_ripple-0.1.0-py3-none-any.whl
```
To then run, simply call `ripple` or `ripple.exe` in any terminal or launcher.

## Have fun!
... or not, I don't care.

Tejune/Project-Ripple is licensed under the GNU General Public License v3.0.
