# -*- mode: python ; coding: utf-8 -*-

import glob
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# --- Chemins ---
project_root = Path.cwd()
config_file = project_root / "ByItsuki-navigateur" / "configuration" / ".config"

# --- Modules cachés ---
hiddenimports = collect_submodules('utils') + collect_submodules('interface')

# --- Fichiers à inclure ---
datas = [
    (str(config_file), "configuration/.config"),  # fichier de config
]

# Ajout des icônes
icons_path = project_root / "ByItsuki-navigateur" / "interface" / "img" / "asset" / "icons"
for f in glob.glob(str(icons_path / "*")):
    datas.append((f, "interface/img/asset/icons"))

# --- Build ---
block_cipher = None

a = Analysis(
    ['ByItsuki-navigateur/interface/page/accueil/principal.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='navigateur-ByItsuki',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False  # mettre True si tu veux voir les logs
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='navigateur'
)
