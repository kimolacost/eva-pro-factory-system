@echo off
title Roblox Blocker / Unblocker
color 0A

:menu
cls
echo ===========================================
echo     Roblox Blocker / Unblocker
echo ===========================================
echo 1. منع Roblox نهائي
echo 2. السماح بـ Roblox
echo 3. خروج
set /p choice=اختر خيارك (1-3): 

if "%choice%"=="1" goto block
if "%choice%"=="2" goto unblock
if "%choice%"=="3" exit
goto menu

:block
cls
echo يمنع Roblox...
:: التحقق من مسار Roblox قبل الحظر
if exist "%localappdata%\Roblox" (
    rd /s /q "%localappdata%\Roblox"
    echo مجلد Roblox تم حذفه.
) else (
    echo مجلد Roblox غير موجود، تابع الحظر.
)
:: تعديل Hosts بطريقة آمنة
set hostsfile=%windir%\System32\drivers\etc\hosts
findstr /i "roblox.com rbxcdn.com setup.roblox.com" %hostsfile% >nul
if errorlevel 1 (
    echo 127.0.0.1 roblox.com>>%hostsfile%
    echo 127.0.0.1 www.roblox.com>>%hostsfile%
    echo 127.0.0.1 rbxcdn.com>>%hostsfile%
    echo 127.0.0.1 setup.roblox.com>>%hostsfile%
)
:: الحظر عبر Firewall بطريقة متقدمة
for /D %%i in ("%localappdata%\Roblox\Versions\*") do (
    if exist "%%i\RobloxPlayerBeta.exe" (
        netsh advfirewall firewall add rule name="Block Roblox Player" dir=out action=block program="%%i\RobloxPlayerBeta.exe"
    )
    if exist "%%i\RobloxStudioBeta.exe" (
        netsh advfirewall firewall add rule name="Block Roblox Studio" dir=out action=block program="%%i\RobloxStudioBeta.exe"
    )
)
echo Roblox تم منعه نهائي!
pause
goto menu

:unblock
cls
echo السماح بـ Roblox...
:: إزالة Roblox من Hosts
powershell -Command "(gc %windir%\System32\drivers\etc\hosts) -notmatch 'roblox' | Out-File -encoding ASCII %windir%\System32\drivers\etc\hosts"
:: إزالة قواعد Firewall
netsh advfirewall firewall delete rule name="Block Roblox Player"
netsh advfirewall firewall delete rule name="Block Roblox Studio"
echo Roblox أصبح مسموح الآن!
pause
goto menu
