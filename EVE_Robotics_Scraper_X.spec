# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\dimka\\Documents\\GitHub\\EVE_Robotics_Scraper_X'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=True,
             win_private_assemblies=True,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='EVE_Robotics_Scraper_X',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True , uac_uiaccess=True, icon='app\\uix\\ico.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='EVE_Robotics_Scraper_X')
