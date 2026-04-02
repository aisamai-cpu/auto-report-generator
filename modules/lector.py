import pandas as pd

def detectar_tabla(ruta):
    if ruta.endswith('.xlsx') or ruta.endswith('.xls'):
        excel = pd.ExcelFile(ruta)
        hoja = excel.sheet_names[0]
        df_raw = pd.read_excel(ruta, sheet_name=hoja, header=None)
    else:
        df_raw = pd.read_csv(ruta, header=None)

    # Buscar la fila donde empieza la tabla
    for i, fila in df_raw.iterrows():
        valores = fila.dropna()
        if len(valores) >= 2:
            header_row = i
            break

    if ruta.endswith('.xlsx') or ruta.endswith('.xls'):
        df = pd.read_excel(ruta, sheet_name=hoja, header=header_row)
    else:
        df = pd.read_csv(ruta, header=header_row)

    df = df.dropna(how='all')
    df.columns = df.columns.astype(str).str.strip()
    return df

def cargar_con_mapeo(df, mapeo):
    df_nuevo = pd.DataFrame()
    df_nuevo['mes'] = df[mapeo['mes']].astype(str).str.strip()
    df_nuevo['producto'] = df[mapeo['producto']].astype(str).str.strip()
    df_nuevo['categoria'] = df[mapeo['categoria']].astype(str).str.strip()
    df_nuevo['ventas'] = pd.to_numeric(df[mapeo['ventas']], errors='coerce').fillna(0)
    df_nuevo['unidades'] = pd.to_numeric(df[mapeo['unidades']], errors='coerce').fillna(0)
    df_nuevo = df_nuevo.dropna(subset=['mes', 'producto', 'ventas'])
    df_nuevo = df_nuevo[df_nuevo['mes'] != 'nan']
    return df_nuevo

def resumen_general(df):
    total_ventas = df['ventas'].sum()
    promedio_periodo = df.groupby('mes')['ventas'].sum().mean()
    mejor_periodo = df.groupby('mes')['ventas'].sum().idxmax()
    mejor_producto = df.groupby('producto')['ventas'].sum().idxmax()

    return {
        'total_ventas': total_ventas,
        'promedio_mensual': round(promedio_periodo, 2),
        'mejor_mes': mejor_periodo,
        'mejor_producto': mejor_producto
    }

def ventas_por_mes(df):
    orden = list(df['mes'].unique())
    return df.groupby('mes')['ventas'].sum().reindex(orden)

def ventas_por_producto(df):
    return df.groupby('producto')['ventas'].sum().sort_values(ascending=False)