# 📊 Auto Report Generator

Herramienta de automatización en Python que convierte cualquier archivo Excel o CSV de ventas en un reporte PDF profesional con gráficas y tablas automáticamente.

## 🚀 ¿Qué hace?

- Lee cualquier archivo Excel o CSV sin importar su formato
- Detecta automáticamente dónde está la tabla de datos
- Permite al usuario mapear sus propias columnas (sin importar cómo las llamó)
- Genera gráfica de barras por periodo (dia, semana, mes, año)
- Genera gráfica de distribución por producto
- Exporta un reporte PDF profesional con resumen ejecutivo y tabla de detalle
- Interfaz gráfica simple, sin necesidad de conocimientos técnicos
## 🖥️ Interfaz

El usuario solo necesita:
1. Abrir la aplicación
2. Seleccionar su archivo Excel o CSV
3. Indicar qué columna corresponde a cada campo
4. Hacer clic en "Generar Reporte PDF"

## ⚙️ Instalacion

1. Clona el repositorio:
```bash
git clone https://github.com/aisamai-cpu/auto-report-generator.git
cd auto-report-generator
```
2. Crea y activa el entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Uso

Con interfaz grafica:
```bash
python app.py
```
Por terminal:
```bash
python main.py
```
## 📋 Formato del archivo de entrada

El archivo Excel o CSV debe tener al menos estas columnas (con cualquier nombre):
- **Periodo** — dia, semana, mes o año
- **Producto** — nombre del producto o servicio
- **Categoria** — tipo o categoria del producto
- **Ventas** — monto total de ventas
- **Unidades** — cantidad vendida

La tabla puede estar en cualquier parte del archivo. La app detecta las columnas automaticamente.

## 🛠️ Tecnologias

- Python 3
- pandas
- matplotlib
- fpdf2
- openpyxl
- tkinter

## 📄 Ejemplo de reporte generado

El reporte PDF incluye:
- Resumen ejecutivo con metricas clave
- Grafica de ventas por periodo
- Distribucion de ventas por producto
- Tabla detallada de ventas

---
Desarrollado por Aarón Isama