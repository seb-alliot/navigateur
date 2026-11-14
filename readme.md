# Web Browser (Under Development)

## Useful links

- **Python** → [python](https://www.python.org/downloads/)
- **PySide6** → [Pyside](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html)
- **Trello** → [trello](https://trello.com/invite/b/68ff227bb886545dbb60d6f7/ATTI2b2f3b86624d3ffd359c1ab95d13b7f98E33DA0E/navigateur)
- **GitHub** → [github](https://github.com/seb-alliot/navigateur.git)

## Technologies

Python 3.13, PySide6

This project is a minimal web browser currently under development. The interface is the main focus for now, while a custom search engine will be implemented later.

## Installation Instructions

### Install Python 3.13

Make sure to check “Add Python to PATH” during installation.

### Install project dependencies

Dependencies are added gradually as the project progresses.

Use the `requirements.txt` file to install the necessary modules:

```bash
pip install -r requirements.txt
```

## Compilation

### With PyInstaller

```bash
pyinstaller --onefile --noconsole --name Navigateur-ByItsuki --add-data "ByItsuki-navigateur\configuration\.config;configuration" ByItsuki-navigateur\interface\page\principal\principal.py
```

or

```bash
pyinstaller navigateur.spec
```

### With Nuitka

```bash
cd ByItsuki-navigateur
python -m nuitka --onefile --enable-plugin=pyside6 --windows-console-mode=disable --windows-icon-from-ico=interface/img/asset/icons/ByItsuki.ico --include-data-dir=interface=interface --include-data-dir=utils=utils --include-data-dir=configuration=configuration --output-filename="Navigateur-ByItsuki.exe" interface/page/principal/principal.py
```
```
