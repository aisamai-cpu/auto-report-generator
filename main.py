import os
from modules.lector import cargar_datos, resumen_general, ventas_por_mes, ventas_por_producto
from modules.graficas import grafica_ventas_por_mes, grafica_ventas_por_producto
from modules.generador import generar_reporte

# Rutas
RUTA_DATOS = 'data/ventas.csv'
RUTA_GRAFICA_MES = 'output/grafica_mes.png'
RUTA_GRAFICA_PRODUCTO = 'output/grafica_producto.png'
RUTA_REPORTE = 'output/reporte_ventas.pdf'

def main():
    print("📂 Cargando datos...")
    df = cargar_datos(RUTA_DATOS)

    print("🔍 Procesando información...")
    resumen = resumen_general(df)
    ventas_mes = ventas_por_mes(df)
    ventas_producto = ventas_por_producto(df)

    print("📊 Generando gráficas...")
    grafica_ventas_por_mes(ventas_mes, RUTA_GRAFICA_MES)
    grafica_ventas_por_producto(ventas_producto, RUTA_GRAFICA_PRODUCTO)

    print("📄 Creando reporte PDF...")
    generar_reporte(resumen, ventas_mes, ventas_producto,
                    RUTA_GRAFICA_MES, RUTA_GRAFICA_PRODUCTO, RUTA_REPORTE)

if __name__ == '__main__':
    main()