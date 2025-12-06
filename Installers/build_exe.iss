[Setup]
; ==============================================================================
; 📝 CONFIGURATION: EDIT THESE LINES FOR EACH PROJECT
; ==============================================================================
AppName=OrnamentBuddy
AppVersion=1.0.0
DefaultGroupName=OrnamentBuddy
;
; EDIT: The folder name created in %APPDATA%. 
; Usually matches your Repo Name.
DefaultDirName={userappdata}\Autodesk\Autodesk Fusion 360\API\AddIns\OrnamentBuddy
;
; EDIT: The Output Filename
OutputBaseFilename=OrnamentBuddyInstaller_Win
;
; LICENSE: Looks in the resources folder in the parent directory
LicenseFile=..\resources\License.rtf
;==============================================================================

PrivilegesRequired=lowest
Compression=lzma
SolidCompression=yes
OutputDir=.

[Files]
; ==============================================================================
; SOURCE FILES
; ==============================================================================
; ".." means "The Parent Directory" (The Root of your Repo)
; We EXCLUDE the 'Installers' folder, .git, and VSCode settings.
Source: "..\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "Installers,.git,.gitignore,.vscode,__pycache__"

[Icons]
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"