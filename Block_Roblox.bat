@echo off
echo يمنع Roblox الآن...
:: إضافة الحظر على مواقع Roblox
set hostsfile=%windir%\System32\drivers\etc\hosts
echo 127.0.0.1 roblox.com>>%hostsfile%
echo 127.0.0.1 www.roblox.com>>%hostsfile%
echo 127.0.0.1 rbxcdn.com>>%hostsfile%
echo 127.0.0.1 setup.roblox.com>>%hostsfile%
echo تم منع Roblox نهائي! حتى مع VPN
pause
