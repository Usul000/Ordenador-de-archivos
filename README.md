╔══════════════════════════════════════════════════════════════════════╗
║           ORGANIZADOR DE FOTOS - XIAOMI NOTE 10 PRO                  ║
║                    INSTRUCCIONES DE USO                              ║
╚══════════════════════════════════════════════════════════════════════╝

📋 REQUISITOS PREVIOS:
═══════════════════════════════════════════════════════════════════════

1. Python 3 instalado
   👉 Descarga desde: https://www.python.org/downloads/
   ⚠️  IMPORTANTE: Al instalar, marca "Add Python to PATH"

2. Instalar librería Pillow (para leer datos EXIF de fotos)
   👉 Abre CMD y ejecuta: pip install Pillow


🚀 CÓMO USAR:
═══════════════════════════════════════════════════════════════════════

OPCIÓN 1 - Doble clic (más fácil):
   1. Doble clic en: EJECUTAR_ORGANIZADOR_XIAOMI.bat
   2. Escribe 'SI' cuando te pregunte
   3. Espera a que termine

OPCIÓN 2 - Línea de comandos:
   1. Abre CMD en esta carpeta
   2. Ejecuta: python organizador_fotos_xiaomi.py


📂 LO QUE HACE:
═══════════════════════════════════════════════════════════════════════

✅ Lee fotos de:
   F:\COPIA TOTAL LIMPIA\Xiaomi Note 10 Pro FOTOS\Camera
   F:\COPIA TOTAL LIMPIA\Xiaomi Note 10 Pro FOTOS\Screenshots

✅ Crea estructura organizada:
   F:\COPIA TOTAL LIMPIA\Xiaomi Note 10 Pro FOTOS\FOTOS_ORGANIZADAS\
   ├── Fotos/
   │   ├── 2024/
   │   │   ├── 01 - January/
   │   │   ├── 02 - February/
   │   │   └── ...
   │   └── 2025/
   │       └── 01 - January/
   └── Capturas/
       ├── Captura_20250120_162735.jpg
       ├── Captura_20250120_164210.jpg
       └── ...

✅ Detecta duplicados (por contenido, no por nombre)
✅ Renombra screenshots con nombres limpios
✅ Lee fecha EXIF de las fotos para organizarlas correctamente


⚙️  PERSONALIZACIÓN:
═══════════════════════════════════════════════════════════════════════

Si quieres cambiar la ruta base, edita el archivo:
   organizador_fotos_xiaomi.py

En la línea que dice:
   ruta_base = r"F:\COPIA TOTAL LIMPIA\Xiaomi Note 10 Pro FOTOS"

Y cámbiala por tu ruta.


📊 RESULTADO:
═══════════════════════════════════════════════════════════════════════

Al finalizar verás:
   ✅ Número de fotos organizadas
   ✅ Número de capturas renombradas
   ✅ Número de duplicados eliminados
   ✅ Archivo REPORTE.txt con detalles completos


⚠️  IMPORTANTE:
═══════════════════════════════════════════════════════════════════════

❌ Los archivos originales NO se tocan, solo se COPIAN
❌ Tus fotos y screenshots originales quedan intactas
✅ Todo se guarda en la nueva carpeta FOTOS_ORGANIZADAS/


💡 SOLUCIÓN DE PROBLEMAS:
═══════════════════════════════════════════════════════════════════════

❌ Error: "Python no reconocido"
   → Instala Python y marca "Add Python to PATH"

❌ Error: "No module named 'PIL'"
   → Ejecuta en CMD: pip install Pillow

❌ Error: "No se encuentra la carpeta"
   → Verifica que la ruta en el script sea correcta

❌ El programa no hace nada
   → Asegúrate de escribir 'SI' (en mayúsculas) cuando te pregunte


═══════════════════════════════════════════════════════════════════════
¡Listo! Ahora ejecuta EJECUTAR_ORGANIZADOR_XIAOMI.bat y disfruta de tus
fotos organizadas 📸✨
═══════════════════════════════════════════════════════════════════════
