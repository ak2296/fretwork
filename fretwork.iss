; Fretwork installer (Inno Setup 6). Built automatically by GitHub Actions.
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{8F3C2A51-6D2B-4E7A-9C1E-5B7D3A2F9E01}
AppName=Fretwork
AppVersion={#AppVersion}
AppVerName=Fretwork {#AppVersion}
AppPublisher=Fretwork
DefaultDirName={localappdata}\Programs\Fretwork
DefaultGroupName=Fretwork
DisableProgramGroupPage=yes
DisableDirPage=auto
PrivilegesRequired=lowest
OutputDir=dist
OutputBaseFilename=FretworkSetup
SetupIconFile=fretwork.ico
UninstallDisplayIcon={app}\Fretwork.exe
UninstallDisplayName=Fretwork
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"

[Files]
Source: "dist\Fretwork.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Fretwork"; Filename: "{app}\Fretwork.exe"; Comment: "Guitar practice: drills, scales, riffs, licks and your songs"
Name: "{autodesktop}\Fretwork"; Filename: "{app}\Fretwork.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Fretwork.exe"; Description: "Start Fretwork"; Flags: nowait postinstall skipifsilent
