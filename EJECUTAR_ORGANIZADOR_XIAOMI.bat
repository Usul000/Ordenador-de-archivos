@echo off
chcp 65001 >nul
cls
echo.
echo ========================================================================
echo     ORGANIZADOR DE FOTOS - XIAOMI NOTE 10 PRO
echo ========================================================================
echo.
echo 📸 Este programa va a organizar tus fotos:
echo.
echo   ✅ Fotos de Camera    →  Organizadas por Año/Mes
echo   ✅ Screenshots        →  Renombradas con nombres limpios
echo   ✅ Duplicados         →  Eliminados automáticamente
echo.
echo 📂 El programa te preguntará:
echo    - Carpeta ORIGEN (donde están las fotos ahora)
echo    - Carpeta DESTINO (donde se guardarán organizadas)
echo.
echo 💾 Los archivos originales NO se tocan (solo se copian)
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

REM Verificar que existe el archivo Python
if not exist "%~dp0organizador_fotos_xiaomi.py" (
    echo.
    echo ❌ ERROR: No se encuentra organizador_fotos_xiaomi.py
    echo.
    echo 📂 Archivos necesarios en esta carpeta:
    echo    - organizador_fotos_xiaomi.py
    echo    - EJECUTAR_ORGANIZADOR_XIAOMI.bat  (este archivo)
    echo.
    pause
    exit /b 1
)

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ PYTHON NO ESTÁ INSTALADO
    echo.
    echo 📖 Lee el archivo: INSTALAR_PYTHON.txt
    echo.
    echo 💡 Pasos rápidos:
    echo    1. Ve a: https://www.python.org/downloads/
    echo    2. Descarga Python
    echo    3. ⚠️  MARCA "Add Python to PATH" al instalar
    echo    4. Después ejecuta: pip install Pillow
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Python detectado
echo.
echo 🔍 Verificando librería Pillow...
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Pillow no está instalado. Instalando ahora...
    echo.
    pip install Pillow
    if errorlevel 1 (
        echo.
        echo ❌ Error al instalar Pillow
        echo 💡 Intenta manualmente: pip install Pillow
        echo.
        pause
        exit /b 1
    )
    echo.
    echo ✅ Pillow instalado correctamente
    echo.
)

echo ✅ Todo listo para comenzar
echo.
pause

cls
echo.
echo ========================================================================
echo     INICIANDO ORGANIZADOR...
echo ========================================================================
echo.

python "%~dp0organizador_fotos_xiaomi.py"

if errorlevel 1 (
    echo.
    echo ❌ Hubo un error al ejecutar el programa
    echo.
)

echo.
pause
