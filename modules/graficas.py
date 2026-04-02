import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def grafica_ventas_por_mes(ventas_mes, ruta_salida):
    meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
    ventas_mes = ventas_mes.reindex(meses_orden)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(ventas_mes.index, ventas_mes.values, color='#2E86AB', edgecolor='white', linewidth=0.8)

    for bar, valor in zip(bars, ventas_mes.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                f'${valor:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_title('Ventas Totales por Mes', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Mes', fontsize=11)
    ax.set_ylabel('Ventas ($)', fontsize=11)
    ax.set_ylim(0, ventas_mes.max() * 1.2)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()

def grafica_ventas_por_producto(ventas_producto, ruta_salida):
    fig, ax = plt.subplots(figsize=(8, 5))
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B']
    ax.pie(ventas_producto.values, labels=ventas_producto.index,
           autopct='%1.1f%%', colors=colores[:len(ventas_producto)],
           startangle=140, wedgeprops={'edgecolor': 'white', 'linewidth': 2})

    ax.set_title('Distribución de Ventas por Producto', fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()