# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('modelos/datos.db', 'modelos'), ('recursos/iconos/*.ico', 'recursos/iconos'), ('recursos/img/*.png', 'recursos/img'), ('vistas/*.py', 'vistas'), ('controladores/*.py', 'controladores')],
    hiddenimports=['reportlab.graphics.barcode.code128', 'reportlab.graphics.barcode.code93', 'reportlab.graphics.barcode.code39', 'reportlab.graphics.barcode.eanbc', 'reportlab.graphics.barcode.qr', 'reportlab.graphics.barcode.usps', 'reportlab.graphics.barcode.ecc200', 'reportlab.graphics.barcode.usps4s', 'reportlab.graphics.barcode.ecc200datamatrix'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='turismoPlanning',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['recursos\\iconos\\ic_escritorio.ico'],
)
