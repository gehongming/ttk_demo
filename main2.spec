# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all


block_cipher = None


a = Analysis(['demo2.py'],
             pathex=['F:\venv\.env\open-api\Scripts'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             datas = [],
             binaries = [])
			 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='xmmitmweb',
          debug=True,
          strip=None,
          upx=True,
          console=True,
          entitlements_file=None , icon='icon.ico')
