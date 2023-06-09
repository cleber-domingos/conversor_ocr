; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{4954073A-F5FD-433D-8C5F-DBA63A3674A0}
AppName=APP_OCR
AppVersion=1.0
;AppVerName=APP_OCR 1.0
AppPublisher=Cleber Augusto
AppPublisherURL=https://www.example.com/
AppSupportURL=https://www.example.com/
AppUpdatesURL=https://www.example.com/
DefaultDirName=c:\app_ocr
ChangesAssociations=yes
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=C:\Users\cleberdomingos-bdc\Desktop
OutputBaseFilename=APP_OCR
SetupIconFile=C:\Users\cleberdomingos-bdc\Downloads\ocr (1).ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\cleberdomingos-bdc\Documents\Programacao\conversor_ocr\dist\app_ocr\app_ocr.exe"; DestDir: "c:\app_ocr"; Flags: ignoreversion
Source: "C:\Users\cleberdomingos-bdc\Documents\Programacao\conversor_ocr\Tesseract-OCR\*"; DestDir: "c:\app_ocr"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cleberdomingos-bdc\Documents\Programacao\conversor_ocr\poppler-0.68.0\*"; DestDir: "c:\app_ocr"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\cleberdomingos-bdc\Documents\Programacao\conversor_ocr\dist\app_ocr\*"; DestDir: "c:\app_ocr"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\Classes\.myp\OpenWithProgids"; ValueType: string; ValueName: "APP_OCRFile.myp"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\APP_OCRFile.myp"; ValueType: string; ValueName: ""; ValueData: "APP_OCR File"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\APP_OCRFile.myp\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\app_ocr.exe,0"
Root: HKA; Subkey: "Software\Classes\APP_OCRFile.myp\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\app_ocr.exe"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\app_ocr.exe\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{autoprograms}\APP_OCR"; Filename: "{app}\app_ocr.exe"
Name: "{autodesktop}\APP_OCR"; Filename: "{app}\app_ocr.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\app_ocr.exe"; Description: "{cm:LaunchProgram,APP_OCR}"; Flags: nowait postinstall skipifsilent

