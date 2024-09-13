# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('src\\new_certificazione_770\\assets\\*.png', 'assets'), ('src\\new_certificazione_770\\main.ico', '.')]
datas += collect_data_files('sv_ttk')


a = Analysis(
    ['src\\cli.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['tkcalendar', 'babel.numbers', 'openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='new-certificazione-770',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.rc',
    icon=['src\\new_certificazione_770\\main.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='new-certificazione-770',
)
