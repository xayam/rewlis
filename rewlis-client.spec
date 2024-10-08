# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['rewlis_client.py'],
    pathex=[],
    binaries=[],
    datas=[('./res/img', 'res/img')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorflow', 'pandas', 'numpy', 'sklearn', 'tensorflow_hub', 'tensorflow_text', 'vosk', 'sox', 'gensim', 'chardet'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='rewlis-client',
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
    icon=['res\\img\\icon.ico'],
)
