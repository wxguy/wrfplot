; This script requires 'EnVar_plug-in' plugin from https://nsis.sourceforge.io/EnVar_plug-in.
; Download and extract to NSIS install directory C:\Program Files(x86)

; Define the path to directory where Nutika put all our application files and directories
!define PY_APP_DIR "build\windows\wrfplot" 
!define PRODUCT_NAME "wrfplot"
!define PRODUCT_VERSION "2.0.2"
!define BITNESS "64"
!define ARCH_TAG ".amd64"
!define INSTALLER_NAME "wrfplot-windows-64bit.exe"
!define PRODUCT_ICON "${PY_APP_DIR}\_internal\data\wxguy.ico"
BrandingText 'WRFPLOT by WxGuy'

; Marker file to tell the uninstaller that it's a user installation
!define USER_INSTALL_MARKER _user_install_marker

SetCompressor lzma

!if "${NSIS_PACKEDVERSION}" >= 0x03000000
  Unicode true
  ManifestDPIAware true
!endif

!define MULTIUSER_EXECUTIONLEVEL Highest
!define MULTIUSER_INSTALLMODE_DEFAULT_CURRENTUSER
!define MULTIUSER_MUI
!define MULTIUSER_INSTALLMODE_COMMANDLINE
!define MULTIUSER_INSTALLMODE_INSTDIR "wrfplot"
!define MULTIUSER_INSTALLMODE_FUNCTION correct_prog_files
!include MultiUser.nsh
!include FileFunc.nsh
;!include EnvVarUpdate.nsh

; Modern UI installer stuff
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "${PY_APP_DIR}\_internal\data\wxguy.ico"
!define MUI_UNICON "${PY_APP_DIR}\_internal\data\wxguy.ico"

; UI pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE LICENSE
!insertmacro MULTIUSER_PAGE_INSTALLMODE
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "build\windows\${INSTALLER_NAME}"
ShowInstDetails show

Var cmdLineInstallDir

Section -SETTINGS
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
SectionEnd


Section "!${PRODUCT_NAME}" sec_app
  SetRegView 64
  SectionIn RO
  File ${PRODUCT_ICON} 

  ; Marker file for per-user install
  StrCmp $MultiUser.InstallMode CurrentUser 0 +3
    FileOpen $0 "$INSTDIR\${USER_INSTALL_MARKER}" w
    FileClose $0
    SetFileAttributes "$INSTDIR\${USER_INSTALL_MARKER}" HIDDEN

  ; Install directories
    SetOutPath "$INSTDIR"
    File /r "${PY_APP_DIR}\*.*"

  ; Install shortcuts
  ; The output path becomes the working directory for shortcuts
  SetOutPath "%HOMEDRIVE%\%HOMEPATH%"
    CreateShortCut "$SMPROGRAMS\wrfplot.lnk" "$INSTDIR\wrfplot.exe" "$INSTDIR\_internal\data\wxguy.ico"
  SetOutPath "$INSTDIR"

    DetailPrint "Setting up command-line launcher..."

    StrCmp $MultiUser.InstallMode CurrentUser 0 AddSysPathSystem
      ; Add to PATH for current user
      ; set the variable to machine folder
      EnVar::SetHKCU
      ; Append install dir to PATH
      EnVar::AddValue "PATH" "$INSTDIR"
      Pop $0
      GoTo AddedSysPath
    AddSysPathSystem:
      ; Add to PATH for all users
      ; set the variable to user folder
      EnVar::SetHKLM
      ; Append install dir to PATH
      EnVar::AddValue "PATH" "$INSTDIR"
      Pop $0
    AddedSysPath:

  ; Byte-compile Python files.
  ;DetailPrint "Byte-compiling Python modules..."
  DetailPrint "Add ourselves to Add/remove programs"
  ;nsExec::ExecToLog '"$INSTDIR\Python\python" -m compileall -q "$INSTDIR\pkgs"'
  WriteUninstaller $INSTDIR\uninstall.exe
  ; Add ourselves to Add/remove programs
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "InstallLocation" "$INSTDIR"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayIcon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                     "Publisher" "WxGuy"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegDWORD SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "NoModify" 1
  WriteRegDWORD SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "NoRepair" 1

  ; Check if we need to reboot
  IfRebootFlag 0 noreboot
    MessageBox MB_YESNO "A reboot is required to finish the installation. Do you wish to reboot now?" \
                /SD IDNO IDNO noreboot
      Reboot
  noreboot:
SectionEnd

Section "Uninstall"
  SetRegView 64
  SetShellVarContext all
  IfFileExists "$INSTDIR\${USER_INSTALL_MARKER}" 0 +3
    SetShellVarContext current
    Delete "$INSTDIR\${USER_INSTALL_MARKER}"

  Delete $INSTDIR\uninstall.exe
  Delete "$INSTDIR\${PRODUCT_ICON}"

  ; Remove ourselves from %PATH%
  EnVar::DeleteValue "PATH" "$INSTDIR"
  Pop $0

  ; Uninstall files
    ;Delete "$INSTDIR\wrfplot.ico"
    ;Delete "$INSTDIR\wrfplot.launch.pyw"
    ;Delete "$INSTDIR\LICENSE.md"
    ;Delete "$INSTDIR\_system_path.py"
  

  ; Uninstall shortcuts
      Delete "$SMPROGRAMS\wrfplot.lnk"

  ; Uninstall install directory
  RMDir $INSTDIR
  DeleteRegKey SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"

SectionEnd


; Functions

Function .onMouseOverSection
    ; Find which section the mouse is over, and set the corresponding description.
    FindWindow $R0 "#32770" "" $HWNDPARENT
    GetDlgItem $R0 $R0 1043 ; description item (must be added to the UI)

    StrCmp $0 ${sec_app} "" +2
      SendMessage $R0 ${WM_SETTEXT} 0 "STR:${PRODUCT_NAME}"

FunctionEnd

Function .onInit
  ; Multiuser.nsh breaks /D command line parameter. Parse /INSTDIR instead.
  ; Cribbing from https://nsis-dev.github.io/NSIS-Forums/html/t-299280.html
  ${GetParameters} $0
  ClearErrors
  ${GetOptions} '$0' "/INSTDIR=" $1
  IfErrors +2  ; Error means flag not found
    StrCpy $cmdLineInstallDir $1
  ClearErrors

  !insertmacro MULTIUSER_INIT

  ; If cmd line included /INSTDIR, override the install dir set by MultiUser
  StrCmp $cmdLineInstallDir "" +2
    StrCpy $INSTDIR $cmdLineInstallDir
FunctionEnd

Function un.onInit
  !insertmacro MULTIUSER_UNINIT
FunctionEnd

Function correct_prog_files
  ; The multiuser machinery doesn't know about the different Program files
  ; folder for 64-bit applications. Override the install dir it set.
  StrCmp $MultiUser.InstallMode AllUsers 0 +2
    StrCpy $INSTDIR "$PROGRAMFILES64\${MULTIUSER_INSTALLMODE_INSTDIR}"
FunctionEnd
