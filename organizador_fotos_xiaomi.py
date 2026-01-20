#!/usr/bin/env python3
"""
Organizador de Fotos - Xiaomi Note 10 Pro
Organiza fotos de Camera por fecha y renombra Screenshots
"""

import os
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from PIL import Image
from PIL.ExifTags import TAGS
import re

class OrganizadorFotosXiaomi:
    def __init__(self, ruta_origen, ruta_destino):
        """Inicializa el organizador"""
        self.ruta_origen = Path(ruta_origen)
        self.ruta_destino = Path(ruta_destino)
        
        # Carpetas de origen
        self.carpeta_camera = self.ruta_origen / "Camera"
        self.carpeta_screenshots = self.ruta_origen / "Screenshots"
        
        # Carpetas de salida organizadas
        self.carpeta_fotos_organizadas = self.ruta_destino / "Fotos"
        self.carpeta_screenshots_organizadas = self.ruta_destino / "Capturas"
        
        # Estadísticas
        self.fotos_procesadas = 0
        self.screenshots_renombradas = 0
        self.duplicados_eliminados = 0
        self.errores = []
        
        # Hash para detectar duplicados
        self.hashes_vistos = {}
        
    def calcular_hash(self, filepath):
        """Calcula el hash MD5 de una imagen"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return None
    
    def obtener_fecha_exif(self, filepath):
        """Obtiene la fecha de la foto desde los datos EXIF"""
        try:
            image = Image.open(filepath)
            exif_data = image._getexif()
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "DateTimeOriginal" or tag == "DateTime":
                        # Formato: "2025:01:20 16:27:35"
                        fecha_str = str(value)
                        return datetime.strptime(fecha_str, "%Y:%m:%d %H:%M:%S")
        except:
            pass
        
        # Si no hay EXIF, usar fecha de modificación del archivo
        try:
            timestamp = filepath.stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except:
            return datetime.now()
    
    def es_duplicado(self, filepath):
        """Verifica si una foto es duplicada"""
        file_hash = self.calcular_hash(filepath)
        if not file_hash:
            return False
        
        if file_hash in self.hashes_vistos:
            return True
        
        self.hashes_vistos[file_hash] = str(filepath)
        return False
    
    def organizar_fotos_camera(self):
        """Organiza las fotos de la carpeta Camera por fecha"""
        print("\n" + "="*70)
        print("📸 ORGANIZANDO FOTOS DE CAMERA")
        print("="*70)
        
        if not self.carpeta_camera.exists():
            print(f"❌ No se encuentra la carpeta: {self.carpeta_camera}")
            return
        
        fotos = list(self.carpeta_camera.glob("*"))
        fotos_validas = [f for f in fotos if f.is_file() and f.suffix.lower() in 
                         ['.jpg', '.jpeg', '.png', '.heic', '.raw', '.dng']]
        
        print(f"📊 Encontradas {len(fotos_validas)} fotos")
        
        for i, foto in enumerate(fotos_validas, 1):
            try:
                # Verificar si es duplicado
                if self.es_duplicado(foto):
                    print(f"   [{i}/{len(fotos_validas)}] 🔄 Duplicado: {foto.name}")
                    self.duplicados_eliminados += 1
                    continue
                
                # Obtener fecha de la foto
                fecha = self.obtener_fecha_exif(foto)
                
                # Crear estructura: Fotos/Año/Mes/
                carpeta_año = self.carpeta_fotos_organizadas / fecha.strftime("%Y")
                carpeta_mes = carpeta_año / fecha.strftime("%m - %B")
                carpeta_mes.mkdir(parents=True, exist_ok=True)
                
                # Copiar foto
                destino = carpeta_mes / foto.name
                contador = 1
                while destino.exists():
                    destino = carpeta_mes / f"{foto.stem}_{contador}{foto.suffix}"
                    contador += 1
                
                shutil.copy2(foto, destino)
                self.fotos_procesadas += 1
                
                if i % 10 == 0:
                    print(f"   [{i}/{len(fotos_validas)}] ✅ Procesadas {self.fotos_procesadas} fotos...")
                
            except Exception as e:
                self.errores.append(f"Error en {foto.name}: {e}")
                print(f"   ⚠️  Error: {foto.name}")
        
        print(f"\n✅ Fotos de Camera organizadas: {self.fotos_procesadas}")
        print(f"🔄 Duplicados eliminados: {self.duplicados_eliminados}")
    
    def limpiar_nombre_screenshot(self, nombre_original):
        """Limpia el nombre de una screenshot"""
        # Buscar fecha en formato Screenshot_2025-12-04-09-47-42
        patron_fecha = r'Screenshot[_-](\d{4})[_-](\d{2})[_-](\d{2})[_-](\d{2})[_-](\d{2})[_-](\d{2})'
        match = re.search(patron_fecha, nombre_original)
        
        if match:
            año, mes, dia, hora, minuto, segundo = match.groups()
            fecha_str = f"{año}{mes}{dia}_{hora}{minuto}{segundo}"
            return f"Captura_{fecha_str}"
        
        # Si no hay fecha, usar timestamp del archivo
        return "Captura"
    
    def organizar_screenshots(self):
        """Organiza y renombra las screenshots"""
        print("\n" + "="*70)
        print("📱 ORGANIZANDO Y RENOMBRANDO SCREENSHOTS")
        print("="*70)
        
        if not self.carpeta_screenshots.exists():
            print(f"❌ No se encuentra la carpeta: {self.carpeta_screenshots}")
            return
        
        screenshots = list(self.carpeta_screenshots.glob("*"))
        screenshots_validas = [f for f in screenshots if f.is_file() and f.suffix.lower() in 
                               ['.jpg', '.jpeg', '.png']]
        
        print(f"📊 Encontradas {len(screenshots_validas)} capturas")
        
        # Crear carpeta de capturas organizadas
        self.carpeta_screenshots_organizadas.mkdir(parents=True, exist_ok=True)
        
        for i, screenshot in enumerate(screenshots_validas, 1):
            try:
                # Verificar si es duplicado
                if self.es_duplicado(screenshot):
                    print(f"   [{i}/{len(screenshots_validas)}] 🔄 Duplicado: {screenshot.name}")
                    self.duplicados_eliminados += 1
                    continue
                
                # Limpiar nombre
                nombre_limpio = self.limpiar_nombre_screenshot(screenshot.name)
                
                # Crear nombre único
                destino = self.carpeta_screenshots_organizadas / f"{nombre_limpio}{screenshot.suffix}"
                contador = 1
                while destino.exists():
                    destino = self.carpeta_screenshots_organizadas / f"{nombre_limpio}_{contador}{screenshot.suffix}"
                    contador += 1
                
                shutil.copy2(screenshot, destino)
                self.screenshots_renombradas += 1
                
                if i % 10 == 0 or i == len(screenshots_validas):
                    print(f"   [{i}/{len(screenshots_validas)}] ✅ Renombradas {self.screenshots_renombradas} capturas...")
                
            except Exception as e:
                self.errores.append(f"Error en {screenshot.name}: {e}")
                print(f"   ⚠️  Error: {screenshot.name}")
        
        print(f"\n✅ Screenshots renombradas: {self.screenshots_renombradas}")
    
    def generar_reporte(self):
        """Genera un reporte final"""
        reporte_path = self.ruta_destino / "REPORTE.txt"
        
        with open(reporte_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("REPORTE DE ORGANIZACIÓN - FOTOS XIAOMI NOTE 10 PRO\n")
            f.write("="*70 + "\n\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"📥 Carpeta origen: {self.ruta_origen}\n")
            f.write(f"📤 Carpeta destino: {self.ruta_destino}\n\n")
            
            f.write(f"📸 Fotos organizadas (Camera): {self.fotos_procesadas}\n")
            f.write(f"📱 Screenshots renombradas: {self.screenshots_renombradas}\n")
            f.write(f"🔄 Duplicados eliminados: {self.duplicados_eliminados}\n\n")
            
            f.write("📂 ESTRUCTURA CREADA:\n")
            f.write(f"   {self.ruta_destino}/\n")
            f.write(f"   ├── Fotos/\n")
            f.write(f"   │   ├── 2024/\n")
            f.write(f"   │   │   ├── 01 - January/\n")
            f.write(f"   │   │   └── 02 - February/\n")
            f.write(f"   │   └── 2025/\n")
            f.write(f"   └── Capturas/\n\n")
            
            if self.errores:
                f.write("⚠️  ERRORES:\n")
                for error in self.errores:
                    f.write(f"   - {error}\n")
        
        print(f"\n📄 Reporte generado: {reporte_path}")

def main():
    """Función principal"""
    print("="*70)
    print("📸 ORGANIZADOR DE FOTOS - XIAOMI NOTE 10 PRO")
    print("="*70)
    
    print("\n📋 Este programa va a:")
    print("   1. Organizar fotos de Camera por fecha (Año/Mes)")
    print("   2. Renombrar screenshots con nombres limpios")
    print("   3. Eliminar duplicados automáticamente")
    print("\n✅ Los archivos originales NO se modifican")
    print("✅ Todo se organizará en la carpeta de destino que indiques")
    
    # Preguntar rutas
    print("\n" + "="*70)
    print("📂 CONFIGURACIÓN DE RUTAS")
    print("="*70)
    
    print("\n📥 CARPETA ORIGEN (donde están las fotos ahora):")
    print("   Ejemplo: F:\\COPIA TOTAL LIMPIA\\Xiaomi Note 10 Pro FOTOS inicio (COPIA SEGURIDAD INICIAL)")
    ruta_origen = input("\n   Escribe la ruta completa: ").strip().strip('"')
    
    if not ruta_origen or not os.path.exists(ruta_origen):
        print(f"\n❌ Error: La ruta '{ruta_origen}' no existe.")
        return
    
    print("\n📤 CARPETA DESTINO (donde se guardarán organizadas):")
    print("   Ejemplo: F:\\COPIA TOTAL LIMPIA\\Xiaomi Note 10 Pro FOTOS FINAL")
    ruta_destino = input("\n   Escribe la ruta completa: ").strip().strip('"')
    
    if not ruta_destino:
        print("\n❌ Error: Debes indicar una ruta de destino.")
        return
    
    # Crear carpeta destino si no existe
    try:
        Path(ruta_destino).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"\n❌ Error al crear carpeta destino: {e}")
        return
    
    print("\n" + "="*70)
    print("✅ CONFIGURACIÓN LISTA")
    print("="*70)
    print(f"\n📥 Origen:  {ruta_origen}")
    print(f"📤 Destino: {ruta_destino}")
    
    confirmar = input("\n¿Continuar? (escribe 'SI'): ").strip()
    if confirmar != 'SI':
        print("\n❌ Operación cancelada.")
        return
    
    print("\n" + "="*70)
    print("🚀 INICIANDO ORGANIZACIÓN")
    print("="*70)
    
    try:
        organizador = OrganizadorFotosXiaomi(ruta_origen, ruta_destino)
        
        # Organizar fotos de Camera
        organizador.organizar_fotos_camera()
        
        # Organizar screenshots
        organizador.organizar_screenshots()
        
        # Generar reporte
        print("\n📊 Generando reporte...")
        organizador.generar_reporte()
        
        print("\n" + "="*70)
        print("✅ ORGANIZACIÓN COMPLETADA")
        print("="*70)
        print(f"\n📸 Fotos organizadas: {organizador.fotos_procesadas}")
        print(f"📱 Capturas renombradas: {organizador.screenshots_renombradas}")
        print(f"🔄 Duplicados eliminados: {organizador.duplicados_eliminados}")
        print(f"\n📂 Todo guardado en: {ruta_destino}")
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación interrumpida por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    
    input("\nPresiona Enter para salir...")
