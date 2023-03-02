# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('ttkbootstrap')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\demo\venv\Scripts'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
			 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='openapi_2.9.2',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          entitlements_file=None , icon='icon.ico')
