@echo off
endlocal
rem This file is UTF-8 encoded, so we need to update the current code page while executing it
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

set VIRTUAL_ENV=%~dp0..
echo %VIRTUAL_ENV%

if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(sphinx_venv) %PROMPT%

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set PYTHONPATH=%VIRTUAL_ENV%\Python310
set PYTHONHOME=%VIRTUAL_ENV%\Python310
set VIRTUAL_ENV_PROMPT=(sphinx_venv) 


set rr="HKCU\Console\%%SystemRoot%%_system32_cmd.exe"

reg add %rr% /v "WindowPosition" /t REG_DWORD /d 0x00100010 /f>nul
::WindowPosition表示窗口位置，高四位为上，低四位为左，距屏幕上沿10eH=270，距屏幕左沿140H=320。

reg add %rr% /v "ScreenBufferSize" /t REG_DWORD /d 0x13880096 /f>nul
::ScreenBufferSize表示缓冲区尺寸，高四位为高度，低四位为宽度，高1388H=5000行，宽96H=150列。

reg add %rr% /v "WindowSize" /t REG_DWORD /d 0x00320096 /f>nul
::WindowSize表示窗口尺寸，高四位为高度，低四位为宽度，高32H=50行，宽96H=150列。
::也可以用mode con cols=45 lines=10来设置窗口尺寸，cols设置宽度，lines设置高度。

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)
setlocal enabledelayedexpansion