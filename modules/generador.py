from fpdf import FPDF
from datetime import datetime

class ReporteVentas(FPDF):
    def header(self):
        self.set_fill_color(46, 134, 171)
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 25, 'Reporte Automatico de Ventas', align='C', ln=True)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.cell(0, 10, f'Generado el {fecha}  |  Pagina {self.page_no()}', align='C')

def generar_reporte(resumen, ventas_mes, ventas_producto, ruta_grafica_mes, ruta_grafica_producto, ruta_salida):
    pdf = ReporteVentas()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Resumen ejecutivo
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(46, 134, 171)
    pdf.cell(0, 10, 'Resumen Ejecutivo', ln=True)
    pdf.set_draw_color(46, 134, 171)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    datos = [
        ('Total de Ventas', f"${resumen['total_ventas']:,.2f}"),
        ('Promedio Mensual', f"${resumen['promedio_mensual']:,.2f}"),
        ('Mejor Mes', resumen['mejor_mes']),
        ('Producto Estrella', resumen['mejor_producto']),
    ]

    pdf.set_text_color(0, 0, 0)
    for etiqueta, valor in datos:
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(70, 9, etiqueta + ':')
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 9, valor, ln=True)

    # Grafica de barras
    pdf.ln(6)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(46, 134, 171)
    pdf.cell(0, 10, 'Ventas por Mes', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.image(ruta_grafica_mes, x=10, w=190)

    # Grafica de pie
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(46, 134, 171)
    pdf.cell(0, 10, 'Distribucion por Producto', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.image(ruta_grafica_producto, x=30, w=150)

    # Tabla detallada
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(46, 134, 171)
    pdf.cell(0, 10, 'Detalle de Ventas por Producto', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_fill_color(46, 134, 171)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(100, 9, 'Producto', border=1, fill=True, align='C')
    pdf.cell(90, 9, 'Total Ventas ($)', border=1, fill=True, align='C', ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 11)
    fill = False
    for producto, total in ventas_producto.items():
        pdf.set_fill_color(235, 245, 251) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(100, 8, producto, border=1, fill=True)
        pdf.cell(90, 8, f"${total:,.2f}", border=1, fill=True, align='R', ln=True)
        fill = not fill

    pdf.output(ruta_salida)
    print(f"Reporte generado: {ruta_salida}")