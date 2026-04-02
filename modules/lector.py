import pandas as pd

def cargar_datos(ruta):
    df = pd.read_csv(ruta)
    return df

def resumen_general(df):
    total_ventas = df['ventas'].sum()
    promedio_mensual = df.groupby('mes')['ventas'].sum().mean()
    mejor_mes = df.groupby('mes')['ventas'].sum().idxmax()
    mejor_producto = df.groupby('producto')['ventas'].sum().idxmax()

    return {
        'total_ventas': total_ventas,
        'promedio_mensual': round(promedio_mensual, 2),
        'mejor_mes': mejor_mes,
        'mejor_producto': mejor_producto
    }

def ventas_por_mes(df):
    return df.groupby('mes')['ventas'].sum()

def ventas_por_producto(df):
    return df.groupby('producto')['ventas'].sum().sort_values(ascending=False)