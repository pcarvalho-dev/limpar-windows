@echo off
:: =============================================================================
:: LIMPEZA INTELIGENTE DO WINDOWS
:: Executa o script Python com interface CLI interativa
:: =============================================================================

title Limpeza do Windows

:: Verifica se já está executando como admin
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_script
) else (
    goto :request_admin
)

:request_admin
echo.
echo ┌─────────────────────────────────────────────────────────────┐
echo │         SOLICITANDO PRIVILEGIOS DE ADMINISTRADOR            │
echo └─────────────────────────────────────────────────────────────┘
echo.
echo Para melhores resultados, este script precisa de privilegios
echo de administrador.
echo.
powershell -Command "Start-Process '%~f0' -Verb RunAs"
exit /b

:run_script
:: Muda para o diretório do script
cd /d "%~dp0"

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ┌─────────────────────────────────────────────────────────────┐
    echo │                    ERRO: Python não encontrado               │
    echo └─────────────────────────────────────────────────────────────┘
    echo.
    echo Python não está instalado ou não está no PATH.
    echo.
    echo Por favor, instale Python de: https://python.org
    echo Certifique-se de marcar "Add Python to PATH" na instalação.
    echo.
    pause
    exit /b 1
)

:: Executa o script Python
python "%~dp0limpar_windows.py"

:: Mantém a janela aberta se houver erro
if errorlevel 1 (
    echo.
    echo Ocorreu um erro durante a execução.
    pause
)

exit /b
