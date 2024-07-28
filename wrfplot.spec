# -*- mode: python ; coding: utf-8 -*-
import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

import os
import importlib
block_cipher = None


def include_files(src_dir, dest_dir, startswith=None, endswith=None):
    """ Copy files from source to Pyinstaller packed destination """
    path_list = []
    if os.path.isdir(src_dir):
        for file in os.listdir(src_dir):
            if startswith is not None:
                if file.startswith(startswith):
                    path_list.append((os.path.join(src_dir, file), dest_dir))
            elif endswith is not None:
                if file.endswith(endswith):
                    path_list.append((os.path.join(src_dir, file), dest_dir))

        if startswith is None and endswith is None:
            path_list.append((src_dir, dest_dir))

    return path_list


conda_prefix = os.getenv("CONDA_PREFIX")
libos_files = include_files(os.path.join(conda_prefix, "lib"), os.path.join("shapely", ".libs"), startswith='libgeos')
py_files = include_files('wrfplot', '.', endswith='.py')
# Convert name list path to list to string
mpl_toolkits_dir = list(importlib.import_module('mpl_toolkits').__path__)[0]
mpl_toolkits_module = include_files(mpl_toolkits_dir, 'mpl_toolkits')
colormaps_module =  os.path.dirname(importlib.machinery.PathFinder().find_module("colormaps").get_filename())


a = Analysis(
    ['wrfplot/wrfplot.py'],
    pathex=[],
    binaries=[],
    datas=[('./wrfplot/data', 'data'), (colormaps_module, 'colormaps')] + libos_files + py_files + mpl_toolkits_module,
    hiddenimports=['colormaps', 'tqdm'],
    hookspath=[],
    hooksconfig={},
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
    name='wrfplot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='wrfplot',
)
