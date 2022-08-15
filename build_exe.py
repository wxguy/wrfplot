#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import platform
import psutil
import shutil
from wrfplot._version import __version__

# Define variables that would be used at later stage
version = __version__
project_root = os.path.dirname(os.path.abspath(__file__))
app_src_py_path = os.path.join(project_root, "wrfplot", "wrfplot.py")
linux_req_apps = ["gcc", 'clang', 'ccache', 'patchelf']
data_dir = os.path.join(os.path.dirname(app_src_py_path), "data")
app_icon = os.path.join(os.path.dirname(app_src_py_path), "data", "wrfplot.png")
win_fs = ["ntfs", "fat", "vfat"]
makeself_path = os.path.join("dev", "makeself-2.4.5", "makeself.sh")
pyinst_dest_path = os.path.join("dist", "wrfplot_dist")

# Set platform specific variable options that would form as part of nutika command
if platform.system() == "Windows":
    output_dir = os.path.join(project_root, 'build', 'windows')
    exe_out_name = os.path.join(output_dir, "wrfplot.exe")
    icon_option = "--windows-icon-from-ico=" + app_icon
elif platform.system() == "Linux":
    output_dir = os.path.join(project_root, 'build', 'linux')
    exe_out_name = os.path.join(output_dir, "wrfplot")
    icon_option = "--linux-onefile-icon=" + app_icon

# Set the list of nutika command line options based on above set variables
cmd = ["python -m nuitka",              # Invoke Nutika using existing Python
       "--assume-yes-for-downloads",    # Yes for downloading necessary remote files by Nutika. Only works on windows but does not affect Linux
       "--follow-imports",              # Follow all the imports by application, modules, submodules etc.
       "--onefile",                     # One directory mode that need to be packaged again for distribution. Spped is better
       "--python-flag=-OO",             # Strips comments that are not required for distribution
       "--output-dir=" + output_dir,         # Output directory where all build and distribution files are to be dumped
       "--plugin-enable=numpy",         # Exclusive module support for comples modules such as numpy, pyside6, pyqt etc. See here for complete list https://github.com/Nuitka/Nuitka/blob/develop/Standard-Plugins-Documentation.rst
       "--show-scons",                  # Show output of scon module. Required for reporting bugs at GitHub
       "--include-package=wrfplot",
       " --include-plugin-directory=wrfplot",
       "--show-modules",                # Provide a final summary on included modules
       "--include-data-dir=" + data_dir + "=data",  # Include data directory that are part of wrfplot project
       app_src_py_path,                 # Actual file from which Nutika will take on
       # icon_option,                     # Add icon for program
       "-o " + exe_out_name]               # Output file name for final executable file
       # "| tee dist1/nuitka_lin.log"]   # Show and save the log to file. Required for reporting bugs
       # --follow-import-to=pyproj --follow-import-to=cartopy


# Simple wrapper command to execute command and check the exit status
def execute_cmd(cmd):
    # proc = Popen(cmd, stdout=PIPE, encoding='utf-8')
    # return proc
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
    h = seconds // (60 * 60)
    m = (seconds - h * 60 * 60) // 60
    s = seconds - (h * 60 * 60) - (m * 60)

    # return [h, m, s]
    return("%d hours, %d minutes, %d seconds" % (h, m, s))


def create_makeself():
    """ Create makeself self executable app distribution """

    if os.path.join(pyinst_dest_path, "wrfplot.run"):
        print("Deleting old 'wrfplot.run' file...")
        os.remove(os.path.join(pyinst_dest_path, "wrfplot.run"))

    if os.path.exists(os.path.join(pyinst_dest_path, "wrfplot")):
        print("Creating Linux installer...")
        shutil.copy("installer.sh", pyinst_dest_path)
        print("Executing makeself command to create archive...")
        execute_cmd("bash " + makeself_path + " " + pyinst_dest_path + " " + os.path.join(pyinst_dest_path, "wrfplot.run") + " wrfplot_Linux_Installer " + "./installer.sh")
        if os.path.exists(os.path.join(pyinst_dest_path, "wrfplot.run")):
            print("Please find the final Linux installer at: " + os.path.join(pyinst_dest_path, "wrfplot.run"))
        else:
            print("Failed to create Linux installer...")


# Read script starts from here when this file is executed
if __name__ == "__main__":
    # Check if we are running the script in correct filesystem
    check_fs()
    startTime = time.time()

    """
    # Create the full command line options from above list
    nuitka_cmd = " ".join(cmd)
    print(style.GREEN + "*** Executable is successfully created ***" + style.RESET)
    print()
    print('\n"' + "***" * 7 + nuitka_cmd + '"\n\n' + "***" * 7)
    if execute_cmd(nuitka_cmd):
        # print(style.GREEN + "*** Executable is successfully created ***" + style.RESET)
        print("*** Executable is successfully created ***")
    else:
        print(style.RED + "xxx Error creating executable xxx")
        print("xxx Error creating executable xxx")
    total_time = time.time() - startTime
    print('The script took {0} Min !'.format(convertSeconds(total_time)))
    """
    execute_cmd("pyinstaller --noconfirm --distpath " + pyinst_dest_path + " wrfplot.spec")
    create_makeself()
    total_time = time.time() - startTime
    print('The script took {0}'.format(convertSeconds(total_time)))
