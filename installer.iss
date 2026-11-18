; Inno Setup script for AgriPulse (optional). Compile after running build_windows.bat.
; NOTE: written for convenience; not compiled in the development environment.
[Setup]
AppName=AgriPulse
AppVersion=1.0.0
AppPublisher=AgriPulse
DefaultDirName={autopf}\AgriPulse
DefaultGroupName=AgriPulse
OutputDir=installer_output
OutputBaseFilename=AgriPulse_Setup_1.0.0
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=app\static\images\agripulse.ico
UninstallDisplayIcon={app}\AgriPulse.exe

[Files]
Source: "dist\AgriPulse\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\AgriPulse"; Filename: "{app}\AgriPulse.exe"
Name: "{autodesktop}\AgriPulse"; Filename: "{app}\AgriPulse.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\AgriPulse.exe"; Description: "Start AgriPulse"; Flags: nowait postinstall skipifsilent

; Farm data lives in %LOCALAPPDATA%\AgriPulse and is intentionally NOT removed on uninstall.
