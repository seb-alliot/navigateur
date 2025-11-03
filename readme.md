## Web Browser (Under Development)

## Useful links:

## python ==> https://www.python.org/downloads/
## PySid6 ==> https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html
## trello ==> https://trello.com/invite/b/68ff227bb886545dbb60d6f7/ATTI2b2f3b86624d3ffd359c1ab95d13b7f98E33DA0E/navigateur
## github ==> https://github.com/seb-alliot/navigateur.git

## Technologies: Python 3.13, PySide6

This project is a minimal web browser currently under development. The interface is the main focus for now, while a custom search engine will be implemented later.


## Installation Instructions

Install Python 3.13

Make sure to check “Add Python to PATH” during installation.

## Install project dependencies

Dependencies are added gradually as the project progresses.

Use the requirements.txt file to install the necessary modules:

==>
## pip install -r requirements.txt in console

and for compiled this application

## pyinstaller --onefile --noconsole --name Navigateur-ByItsuki --add-data "ByItsuki-navigateur\configuration\.config;configuration" ByItsuki-navigateur\interface\page\principal\principal.py
==>

## pyinstaller navigateur.spec


## Known Issues

Video player not supported – Possible codec-related issues.

Google account login with autofill – Autofill does not work, probably due to JavaScript; manual input works.

Site https://www.u-campanile-corte.fr/ – CSS does not render correctly when resizing the page.