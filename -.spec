# -*- mode: python -*-

block_cipher = None


a = Analysis(['-'],
             pathex=['C:\\Users\\dimka\\Desktop\\ToPy3Clone'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='-',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , uac_uiaccess=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='-')