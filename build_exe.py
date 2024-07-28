#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Script to build final executables from source """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

wrfplot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with wrfplot. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import time
import platform
import psutil
import shutil
from shutil import which
from wrfplot._version import __version__
from wrfplot.utils import quote
import glob
import subprocess

# Define variables that would be used at later stage
version = __version__
project_root = os.path.dirname(os.path.abspath(__file__))
app_src_py_path = os.path.join(project_root, "wrfplot", "wrfplot.py")
linux_req_apps = ["gcc", 'clang', 'ccache', 'patchelf']
data_dir = os.path.join(os.path.dirname(app_src_py_path), "data")
app_icon = os.path.join(os.path.dirname(app_src_py_path), "data", "wrfplot.png")
win_fs = ["ntfs", "fat", "vfat"]
makeself_path = os.path.join("dev", "makeself-2.4.5", "makeself.sh")
makeself_wrk_path = os.path.join(project_root, "build", "linux", "wrfplot")
pyinst_dest_path = os.path.join("dist", "wrfplot_dist")
conda_prefix = os.getenv("CONDA_PREFIX")
pyproj_lib_trgt_dir = os.path.join("pyproj", "proj")

# Set compilation option
compile_module = 'nuitka'

# Set platform specific variable options that would form as part of nutika command
if platform.system() == "Windows":
    output_dir = os.path.join(project_root, 'build', 'windows')
    exe_out_name = os.path.join(output_dir, "wrfplot.exe")
    icon_option = "--windows-icon-from-ico=" + app_icon
    pyproj_lib_src_dir = os.path.join(conda_prefix, "Library", "share", "proj")
    geos_dll_files = conda_prefix + "\\Lib\\Library\\bin\\geos*.dll"
    geos_trgt_dir = os.path.join("shapely", "DLLs", "\\")
    compiler = "--mingw64"
    nutika_exe_name = 'wrfplot.exe'  # os.path.join(output_dir, 'wrfplot.dist', 'wrfplot.exe')
    frozen_version_file = os.path.join(project_root, "build", "windows", "wrfplot", "_internal", "_version.py")

elif platform.system() == "Linux":
    output_dir = os.path.join(project_root, 'build', 'linux')
    exe_out_name = os.path.join(output_dir, "wrfplot")
    icon_option = "--linux-onefile-icon=" + app_icon
    pyproj_lib_src_dir = os.path.join(conda_prefix, "share", "proj")
    geos_dll_files = conda_prefix + "/lib/libgeos\*so.\*"
    geos_trgt_dir = "shapely/.libs/"
    compiler = ""
    nutika_exe_name = 'wrfplot' #os.path.join(output_dir, 'wrfplot.dist', 'wrfplot')
    frozen_version_file = os.path.join(project_root, "build", "linux", "wrfplot", "_internal", "_version.py")

# Tested on Miniconda Python 3.10.4
# This is the place one need to be carefull. For wrfplot project, netcdf, shapely and pyproj modules were not detected
# automatically. Hence, I added it manually here.
cmd = ["python -m nuitka",  # Invoke Nutika using existing Python
       "--assume-yes-for-downloads",  # Yes for downloading necessary remote files by Nutika
       "--follow-imports",  # Follow all the imports by application, modules, submodules etc.
       "--standalone",  # One directory mode that need to be packaged again for distribution. Spped is better
       "--remove-output",
       "--python-flag=-OO",  # Strips comments that are not required for distribution
       "--noinclude-default-mode=nofollow",
       # uncomment this line if you wish to avoid various tests and bloated modules. But test it before release
       # "--nofollow-import-to=pandas",
       "--output-dir=" + output_dir,  # Output directory where all build and distribution files are to be dumped
       "--plugin-enable=numpy",
       # Exclusive module support for comples modules such as numpy, pyside6, pyqt etc. See here for complete list https://github.com/Nuitka/Nuitka/blob/develop/Standard-Plugins-Documentation.rst
       "--show-scons",  # Show output of scon module. Required for reporting bugs at GitHub
       "--show-modules",  # Provide a final summary on included modules
       "--include-module=netCDF4.utils",
       "--include-module=cftime._strptime",
       # Add necessary modules not included by Nutika. You will get import module error after compilation only
       "--include-module=colormaps",  # Include missing colormaps module
       "--include-package-data=pyproj",  # Add missing data files of modules that are reported during run time
       "--follow-import-to=pyproj",
       # Include puproj data to final directory. Have to patch it later as it did not include automatically
       "--follow-import-to=shapely",  # Ensure that nutika include all shapely related modules
       "--include-package=shapely",  # Include missing shapely module
       "--include-package-data=shapely",
       # Include shapely data to final directory. Have to patch it later as it did not include automatically
       "--include-data-dir=wrfplot/data=data",  # Include data directory that are part of wrfplot project
       "--include-data-dir=wrfplot/colormaps/colormaps=colormaps/colormaps",
       "--include-data-dir=" + pyproj_lib_src_dir + "=" + pyproj_lib_trgt_dir,
       compiler,
       # Include missing data files of pyproj module
       # "--include-data-file=" + geos_dll_files + "=" + geos_trgt_dir,   # Include libgeos* files to proper destination
       app_src_py_path]  # Actual file from which Nutika will take on

# Frame full command line options from above list
nuitka_cmd = " ".join(cmd)

test_cmd_options = ["build/linux/wrfplot/wrfplot",
                    "--input",
                    "../../WRF_TEST_FILES/wrfout_d02_2016-03-31_00_00_00",
                    "--var",
                    "T2",
                    "--output",
                    "~/Documents/wrfplot_output"]

test_cmd = " ".join(test_cmd_options)


# Simple wrapper command to execute command and check the exit status
def execute_cmd(cmd):
    """ Execute command and wait for it to complete

    Args:
        cmd (str): Command to be executed

    Returns:
        bool: True if command exit with 0 or else false
    """

    if os.system(cmd) == 0:
        return True
    else:
        return False


def get_fs_type(path):
    """ Check filesystem for a given path """

    bestMatch = ""
    fsType = ""
    for part in psutil.disk_partitions():
        if path.startswith(part.mountpoint) and len(bestMatch) < len(part.mountpoint):
            fsType = part.fstype
            bestMatch = part.mountpoint

    return fsType.lower()


def check_fs():
    """ Check if we are building under correct filesystem """

    filesystem = get_fs_type(project_root)
    if platform.system == "Linux":
        if filesystem in win_fs:
            sys.exit("Can not compile Linux application under Windows filesystem.\n"
                     "Please copy source code to Linux filesystem and rerun the build script.")


class style():
    """ Give colours to terminal fonts """

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def convertSeconds(seconds):
    """ Convert seconds into human readable hour/ time format

    Args:
        seconds (int): Input seconds which needs to be formated

    Returns:
        str : Nicely formated hours, minutes, seconds for given seconds
     """

    h = seconds // (60 * 60)
    m = (seconds - h * 60 * 60) // 60
    s = seconds - (h * 60 * 60) - (m * 60)

    # return [h, m, s]
    return ("%d hours, %d minutes, %d seconds" % (h, m, s))


def create_makeself():
    """ Create makeself self executable app distribution under Linux """

    if not os.path.exists(makeself_path):
        makeself = "makeself"
    else:
        os.system('chmod +x ' + makeself_path)
        makeself = "bash " + makeself_path

    if os.path.exists(os.path.join(output_dir, "wrfplot.run")):
        print("Deleting old 'wrfplot.run' file...")
        os.remove(os.path.join(output_dir, "wrfplot.run"))

    if os.path.exists(os.path.join(output_dir, "installer.sh")):
        print("Deleting old 'installer.sh' file...")
        os.remove(os.path.join(output_dir, "installer.sh"))

    if os.path.exists(os.path.join(output_dir, "wrfplot.dist")) and os.path.exists(os.path.join(output_dir, "wrfplot")):
        print("Removing previosly created 'wrfplot' directory...")
        shutil.rmtree(os.path.join(output_dir, "wrfplot"))

    if os.path.exists(os.path.join(output_dir, "wrfplot.dist")):
        print("Deleting old 'wrfplot.dist' directory...")
        os.rename(os.path.join(output_dir, "wrfplot.dist"), os.path.join(output_dir, "wrfplot"))

    if os.path.exists(os.path.join(output_dir, "wrfplot")):
        print("Creating Linux installer...")
        shutil.copy("installer.sh", output_dir)
        os.system("chmod +x " + os.path.join(output_dir, "installer.sh"))
        print("Executing makeself command to create archive...")
        execute_cmd(makeself + " " + os.path.join(output_dir) + " " +
                    os.path.join(output_dir, "wrfplot-linux-64bit.run") +
                    " wrfplot_Linux_Installer " + "./installer.sh")
        if os.path.exists(os.path.join(output_dir, "wrfplot.run")):
            print("Please find the final Linux installer at: " + os.path.join(output_dir, "wrfplot.run"))
        else:
            print("Failed to create Linux installer...")
    else:
        print("wrfplot distribution directory does not exist. Hence not creating a Linux installer...")


def test_wrfplt_exe():
    """ Test the final executable before packing for distribution

    Args:
        nil

    Returns:
        bool : True if command executed is successful or else false
    """

    if execute_cmd(test_cmd) is True:
        print("All successfull...")
        return True
    else:
        return False


def copy_files():
    if platform.system() == "Linux":
        shaply_target_lib_dir = os.path.join(output_dir, "wrfplot.dist", "shapely", ".libs")
        pyproj_target_lib_dir = os.path.join(output_dir, "wrfplot.dist", "pyproj")
        if not os.path.exists(shaply_target_lib_dir):
            print("Making lib directory at", shaply_target_lib_dir)
            os.makedirs(shaply_target_lib_dir)
            print("Copying necessary GEOS libraries to shapely libs directory...")
            execute_cmd("cp -rf " + output_dir + "/wrfplot.dist/libgeos*so.* " + shaply_target_lib_dir)
            execute_cmd("cp -rf " + conda_prefix + "/share/proj " + pyproj_target_lib_dir)

    elif platform.system() == "Windows":
        shaply_target_lib_dir = os.path.join(output_dir, 'wrfplot.dist', 'shapely', 'DLLs')
        if not os.path.exists(shaply_target_lib_dir):
            if not os.path.exists(shaply_target_lib_dir):
                print("Making DLL directory at", shaply_target_lib_dir)
                os.makedirs(shaply_target_lib_dir)
            print("Copying necessary GEOS libraries to shapely DLLs directory...")
            shutil.copy(os.path.join(output_dir, 'wrfplot.dist', 'geos.dll'), shaply_target_lib_dir)
            shutil.copy(os.path.join(output_dir, 'wrfplot.dist', 'geos_c.dll'), shaply_target_lib_dir)


def create_win_exe():
    print('Executing ==>', nuitka_cmd, '\n\n')
    # It will take loong time to compile. Please waaait...
    execute_cmd(nuitka_cmd)


def create_linux_exe():
    print('Executing ==>', nuitka_cmd, '\n\n')
    # It will take loong time to compile. Please waaait...
    execute_cmd(nuitka_cmd)


def create_nsis_installer():
    if platform.system() == 'Windows':
        print("Still work in progress...")
        nsis = os.path.join("C:\\", "Program Files (x86)", "NSIS", "makensis.exe")
        if not os.path.exists(nsis):
            nsis = "makensis.exe"
        nsi_installer_path = "installer.nsi"
        print("Executing ==>", os.path.join(quote(nsis)) + " " + nsi_installer_path)
        # print(os.path.join(quote(nsis)) + " " + nsi_installer_path)
        if execute_cmd(os.path.join(quote(nsis)) + " " + nsi_installer_path) is True:
            print("makensis.exe is successfully executed")


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    return which(name) is not None


def check_linux_exes():
    print("Checking if all necessary linux applications are installed in host system...\n")
    for exe in linux_req_apps:
        if not is_tool(exe):
            sys.exit("You need to install " + " ".join(linux_req_apps) + " to get nuitka working properly.")
        else:
            print("Executable '" + exe + "' is installed...")
    if is_tool("gcc-7"):
        print("'gcc-7' is available...")
        print("Setting CC to 'gcc-7' for maximum compatability...")
        os.system("export CC=gcc-7")
        os.environ["CC"] = "gcc-7"
    elif is_tool("gcc-8"):
        print("'gcc-8' is available...")
        print("Setting CC to 'gcc-8' for maximum compatability...")
        os.environ["CC"] = "gcc-8"
    else:
        os.environ["CC"] = "gcc"


def main():
    if platform.system() == "Windows":
        print("Creating distribution files under Windows...\n\n")
        if compile_module == 'nuitka':
            create_win_exe()
            copy_files()
            create_nsis_installer()
        else:
            print("Using pyinstaller as backend for creating final executable...")
            execute_cmd("pyinstaller --noconfirm --distpath " + output_dir + " wrfplot.spec")            
            if os.path.exists(os.path.join("build", "windows", "wrfplot", 'wrfplot.exe')): 
                print("wrfplot.exe successfully created at :", os.path.exists(os.path.join("build", "windows", "wrfplot", 'wrfplot.exe')))
                print("Creating setup file using NSIS...")
                create_nsis_installer()
            else:
                print('Failed to create wrfplot windows executable...')

    elif platform.system() == "Linux":
        # execute_cmd("pyinstaller --noconfirm --distpath " + pyinst_dest_path + " wrfplot.spec")
        # create_makeself()

        print("Creating distribution files under Linux...")
        if compile_module == 'nuitka':
            check_linux_exes()
            print("Using nuitka as backend for compiling source code...")
            create_linux_exe()
            copy_files()

        else:
            print("Using pyinstaller as backend for creating final executable...")
            execute_cmd("pyinstaller --noconfirm --distpath " + output_dir + " wrfplot.spec")

        # test_wrfplt_exe()
        update_verion()
        create_makeself()


def clean_dirs():
    if os.path.isdir('wrfplot.egg-info'):
        shutil.rmtree('wrfplot.egg-info')
    if os.path.exists(os.path.join(project_root, 'build')) and len(os.listdir(os.path.join(project_root, 'build'))) > 0:
        files = glob.glob(os.path.join(project_root, 'build', '*'))
        for f in files:
            if os.path.isdir(f):
                print("Removing directory", quote(f))
                shutil.rmtree(f)
            elif os.path.isfile(f):
                print("Removing file", quote(f))
                os.remove(f)


def build_sdist():
    if os.system("python -m build --sdist") == 0:
        print("Successfully built source distribution package under 'dist' directory...")
        return True
    else:
        sys.exit("Failure to build source distribution package.\n Please correct the issue and build the executable again.")


def update_verion():
    VERSION = os.listdir(os.path.join(project_root, 'dist'))[0].replace("wrfplot-", "").replace(".tar.gz", "")
    print("Updating varion information to file with :", VERSION)
    print("Version information will be updated in : " + frozen_version_file)
    with open(frozen_version_file, "w") as _file:
        _file.write("# Generated by wrfplot build file. Do not edit it manually...\n")
        _file.write("__version__ = version = " + quote(VERSION))
        _file.write('\n')

   
# Read script starts from here when this file is executed
if __name__ == "__main__":
    # Decide wheather to build using nuitka or pyinstaller
    if len(sys.argv) > 1 and sys.argv[1] == "pyinstaller":
        compile_module = "pyinstaller"
    # Check if we are running the script in correct filesystem
    check_fs()
    clean_dirs()
    build_sdist()
    # sys.exit()
    startTime = time.time()
    main()
    total_time = time.time() - startTime
    print('The script took {0}'.format(convertSeconds(total_time)))
