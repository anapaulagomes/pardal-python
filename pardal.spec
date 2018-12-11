# -*- mode: python -*-
from datetime import datetime
import os
import shutil
import sys

block_cipher = None


main_script = 'pardal/run.py'
if sys.platform.startswith('win'):
    main_script = 'pardal\\run.py'
name = f'pardal-{sys.platform}-{datetime.now().strftime("%d-%m-%y_%H-%M-%S")}'


a = Analysis([main_script],
             pathex=[os.getcwd()],
             binaries=[(shutil.which('flask'), 'flask')],
             hiddenimports=['pyttsx3.drivers.espeak', 'pyttsx3.drivers.nsss', 'pyttsx3.drivers.sapi5', 'flask'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=name,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

shutil.copyfile('keyboard.ini.sample', '{0}/keyboard.ini'.format(DISTPATH))
