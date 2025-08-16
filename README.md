# Manual: Preparación y uso de ESP32 con MicroPython y mpremote (Windows)

## 1. Instalación del driver CP210x

1. Ir a la página oficial de Silicon Labs:
   [https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers)
2. Descargar el paquete para Windows (`CP210x_Windows_Drivers.zip`).
3. Descomprimir el archivo ZIP.
4. Ejecutar **`CP210xVCPInstaller_x64.exe`** (Windows 64 bits) o `..._x86.exe` (Windows 32 bits).
5. Conectar el ESP32 y abrir **Administrador de dispositivos** (`Win + R` → `devmgmt.msc`) para confirmar:

   ```
   Puertos (COM y LPT) → Silicon Labs CP210x USB to UART Bridge (COMx)
   ```

   *(El número COM puede variar, úsalo en los comandos siguientes.)*

---

## 2. Instalación de MicroPython en el ESP32

1. **Instalar Python** (si no está instalado) y agregarlo al PATH.
2. **Instalar esptool**:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install esptool
   ```
3. **Descargar firmware MicroPython**:
   [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/) → versión *GENERIC*.
   
5. **Borrar la memoria flash**:

   ```bash
   python -m esptool --chip esp32 --port COMx erase-flash
   ```
6. **Grabar MicroPython**:

   ```bash
   python -m esptool --chip esp32 --port COMx write-flash -z 0x1000 C:\ruta\al\firmware.bin
   ```

   *(Reemplaza `COMx` por tu puerto y `firmware.bin` por el nombre del archivo descargado.)*

---

## 3. Instalación de mpremote

1. Actualizar pip:

   ```bash
   python -m pip install --upgrade pip
   ```
2. Instalar mpremote desde PyPI:

   ```bash
   python -m pip install mpremote
   ```
3. Verificar instalación:

   ```bash
   python -m mpremote --help
   ```

---

## 4. Uso básico de mpremote

### Conectarse a la REPL

```bash
python -m mpremote connect COMx repl
```

Comandos útiles dentro de REPL:

* **Ctrl+C**: interrumpe ejecución
* **Ctrl+D**: reinicio suave (soft reset)

Prueba:

```python
import sys
print(sys.platform, sys.version)
```

### Manejo de archivos

* **Listar archivos en el ESP32**:

```bash
python -m mpremote connect COMx fs ls
```

* **Subir archivo local como main.py**:

```bash
python -m mpremote connect COMx fs cp main.py :/main.py
```

* **Descargar archivo desde el ESP32**:

```bash
python -m mpremote connect COMx fs cp :/boot.py boot.py
```

* **Borrar archivo en el ESP32**:

```bash
python -m mpremote connect COMx fs rm :/main.py
```

### Ejecutar scripts

* **Ejecutar un script local sin guardarlo**:

```bash
python -m mpremote connect COMx run script.py
```

* **Reiniciar el ESP32**:

```bash
python -m mpremote connect COMx reset
```

### Montar carpeta local para desarrollo rápido

Desde la carpeta de tu proyecto:

```bash
python -m mpremote connect COMx mount .
```

En la REPL podrás importar módulos locales directamente.

---

## 5. Ejemplo mínimo de prueba

**blink.py**

```python
from machine import Pin
import time
led = Pin(2, Pin.OUT)  # LED integrado en muchas DevKit V1
for _ in range(10):
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)
print("Blink ok")
```

**Ejecutar directamente**:

```bash
python -m mpremote connect COMx run blink.py
```

**Guardar como main.py**:

```bash
python -m mpremote connect COMx fs cp blink.py :/main.py
python -m mpremote connect COMx reset
```

---

## 6. Solución de problemas

* **Acceso denegado / Port busy**: cierra cualquier programa que esté usando COMx (Arduino IDE, Thonny, etc.).
* **No aparece el puerto**: revisar en Administrador de dispositivos y reinstalar driver CP210x.
* **Sin respuesta en REPL**: presionar botón RESET/EN del ESP32 y volver a conectar.
* **Cable USB**: usar uno de datos, no solo de carga.

---

Con este flujo, puedes programar y controlar tu ESP32 con MicroPython usando únicamente `mpremote`.
