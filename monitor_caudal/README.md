# Monitor de Flow (CS Service Flow Sensors)

Programa de escritorio que:

1. Captura, por reconocimiento óptico (OCR), el dato **Flow (Nm3/h)** que
   muestra el software *CS Service Flow Sensors* en una región de pantalla
   que tú seleccionas.
2. Cada vez que ese valor cambia, lo registra junto con la hora y el
   **valor que tú ingreses manualmente** (el cual se mantiene igual hasta
   que ingreses uno nuevo).
3. Guarda cada lectura en un archivo Excel (`flow_log.xlsx`).
4. Muestra una gráfica en vivo, en una ventana aparte, de Flow capturado
   vs. valor ingresado.
5. Tiene botones **Iniciar** y **Detener**.

## 1. Instalar Python y dependencias

Necesitas Python 3.9+ instalado en tu PC.

```bash
cd monitor_caudal
pip install -r requirements.txt
```

## 2. Instalar Tesseract OCR (obligatorio)

El OCR lo hace la librería `pytesseract`, pero esta necesita el programa
**Tesseract-OCR** instalado en Windows:

1. Descarga el instalador desde:
   https://github.com/UB-Mannheim/tesseract/wiki
2. Instálalo (ruta por defecto: `C:\Program Files\Tesseract-OCR\tesseract.exe`).
3. Si el programa no lo detecta automáticamente, define la variable de
   entorno `TESSERACT_CMD` con la ruta al `.exe`, por ejemplo en PowerShell:

   ```powershell
   $env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

## 3. Ejecutar el programa

```bash
python app.py
```

## 4. Cómo usarlo

1. Abre también el software **CS Service Flow Sensors** y ubica el
   número del dato **Flow** en pantalla.
2. En el Monitor de Flow, haz clic en **"Seleccionar región del dato
   Flow"**: la pantalla se oscurece, arrastra un rectángulo pequeño que
   cubra solo el número (sin unidades ni texto extra) y suelta el clic.
3. Haz clic en **"Probar lectura"** para confirmar que el número se
   reconoce bien. Si no detecta nada o lee mal, vuelve a seleccionar la
   región ajustando el recuadro (que quede bien ajustado al número, sin
   espacios de más).
4. Escribe un valor inicial en **"Valor a ingresar"** y presiona
   **"Enviar valor"** (o Enter).
5. Haz clic en **"Iniciar"**. Desde ese momento, cada vez que el Flow
   capturado cambie se guardará una fila en `flow_log.xlsx` con:
   fecha/hora, Flow leído y el valor ingresado vigente.
6. Cuando quieras, escribe un nuevo valor y presiona "Enviar valor":
   la gráfica y el Excel seguirán registrando el Flow, ahora comparado
   contra este nuevo valor, hasta que ingreses otro.
7. Haz clic en **"Abrir gráfica"** para ver, en una ventana aparte, el
   Flow capturado (línea azul) contra el valor ingresado (línea roja
   tipo escalón), actualizándose cada segundo.
8. Haz clic en **"Detener"** para pausar la captura. El Excel y la
   gráfica conservan todo lo registrado; puedes volver a "Iniciar"
   cuando quieras.

## Notas y ajustes

- El intervalo de muestreo se controla con `POLL_INTERVAL_SECONDS` en
  `app.py` (por defecto 1 segundo).
- El nombre del Excel se controla con `EXCEL_PATH` en `app.py`. Si el
  archivo ya existe, el programa sigue agregando filas al final en vez
  de sobrescribirlo.
- Si el número tiene coma decimal (ej. `12,5`), el programa la interpreta
  igual que un punto decimal.
- Estructura del proyecto:
  - `app.py` – ventana principal y lógica de la aplicación.
  - `capture.py` – captura de pantalla y OCR del número.
  - `region_selector.py` – selector visual de la región de pantalla.
  - `data_store.py` – almacén de datos compartido con la gráfica.
  - `excel_logger.py` – registro de cada lectura en Excel.
  - `plotting.py` – ventana con la gráfica en vivo.
