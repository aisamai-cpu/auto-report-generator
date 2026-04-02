import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from modules.lector import detectar_tabla, cargar_con_mapeo, resumen_general, ventas_por_mes, ventas_por_producto
from modules.graficas import grafica_ventas_por_mes, grafica_ventas_por_producto
from modules.generador import generar_reporte

RUTA_GRAFICA_MES = 'output/grafica_mes.png'
RUTA_GRAFICA_PRODUCTO = 'output/grafica_producto.png'
RUTA_REPORTE = 'output/reporte_ventas.pdf'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Reportes de Ventas")
        self.root.geometry("500x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")
        self.archivo = None
        self.df_raw = None
        self.columnas = []
        self.mapeo_vars = {}

        # Titulo
        tk.Label(root, text="Generador de Reportes de Ventas",
                 font=("Helvetica", 16, "bold"), bg="#2E86AB", fg="white",
                 pady=15).pack(fill="x")

        # Subtitulo
        tk.Label(root, text="Selecciona tu archivo de ventas (.csv o .xlsx)",
                 font=("Helvetica", 10), bg="#f0f4f8", fg="#444",
                 pady=8).pack()

        # Boton seleccionar archivo
        tk.Button(root, text="📂  Seleccionar archivo de ventas",
                  font=("Helvetica", 11), bg="#2E86AB", fg="white",
                  padx=10, pady=8, relief="flat", cursor="hand2",
                  command=self.seleccionar_archivo).pack(pady=5)

        # Label archivo
        self.label_archivo = tk.Label(root, text="Ningun archivo seleccionado",
                                      font=("Helvetica", 9), bg="#f0f4f8", fg="#888")
        self.label_archivo.pack()

        # Frame mapeo columnas
        self.frame_mapeo = tk.Frame(root, bg="#f0f4f8")
        self.frame_mapeo.pack(pady=5, fill="x", padx=30)

        # Boton generar
        self.btn_generar = tk.Button(root, text="▶  Generar Reporte PDF",
                                     font=("Helvetica", 12, "bold"), bg="#27ae60", fg="white",
                                     padx=15, pady=10, relief="flat", cursor="hand2",
                                     command=self.generar, state="disabled")
        self.btn_generar.pack(pady=10)

        # Estado
        self.label_estado = tk.Label(root, text="",
                                     font=("Helvetica", 10), bg="#f0f4f8", fg="#2E86AB")
        self.label_estado.pack()

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de ventas",
            filetypes=[("Archivos CSV y Excel", "*.csv *.xlsx *.xls")]
        )
        if ruta:
            self.archivo = ruta
            nombre = os.path.basename(ruta)
            self.label_archivo.config(text=f"✅ {nombre}", fg="#27ae60")
            try:
                from modules.lector import detectar_tabla
                self.df_raw = detectar_tabla(ruta)
                self.columnas = list(self.df_raw.columns)
                self.mostrar_mapeo()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def mostrar_mapeo(self):
        for widget in self.frame_mapeo.winfo_children():
            widget.destroy()

        tk.Label(self.frame_mapeo, text="Indica que columna corresponde a cada campo:",
                 font=("Helvetica", 9, "bold"), bg="#f0f4f8", fg="#444").grid(
                 row=0, column=0, columnspan=2, pady=5)

        campos = [
            ('mes', 'Periodo (mes/semana/dia/año)'),
            ('producto', 'Producto o servicio'),
            ('categoria', 'Categoria'),
            ('ventas', 'Ventas (monto $)'),
            ('unidades', 'Unidades vendidas'),
        ]

        self.mapeo_vars = {}
        for i, (campo, etiqueta) in enumerate(campos, 1):
            tk.Label(self.frame_mapeo, text=etiqueta + ":",
                     font=("Helvetica", 9), bg="#f0f4f8", fg="#444",
                     anchor="w").grid(row=i, column=0, sticky="w", pady=2)

            var = tk.StringVar()
            # Intentar autodetectar
            for col in self.columnas:
                if campo in col.lower():
                    var.set(col)
                    break
            else:
                var.set(self.columnas[0])

            combo = ttk.Combobox(self.frame_mapeo, textvariable=var,
                                 values=self.columnas, state="readonly", width=20)
            combo.grid(row=i, column=1, sticky="w", padx=10, pady=2)
            self.mapeo_vars[campo] = var

        self.btn_generar.config(state="normal")
        self.root.geometry("500x550")

    def generar(self):
        self.btn_generar.config(state="disabled")
        self.label_estado.config(text="Procesando...", fg="#2E86AB")
        threading.Thread(target=self.proceso).start()

    def proceso(self):
        try:
            mapeo = {campo: var.get() for campo, var in self.mapeo_vars.items()}
            os.makedirs("output", exist_ok=True)
            df = cargar_con_mapeo(self.df_raw, mapeo)
            resumen = resumen_general(df)
            ventas_mes = ventas_por_mes(df)
            ventas_producto = ventas_por_producto(df)
            grafica_ventas_por_mes(ventas_mes, RUTA_GRAFICA_MES)
            grafica_ventas_por_producto(ventas_producto, RUTA_GRAFICA_PRODUCTO)
            generar_reporte(resumen, ventas_mes, ventas_producto,
                            RUTA_GRAFICA_MES, RUTA_GRAFICA_PRODUCTO, RUTA_REPORTE)
            self.root.after(0, self.exito)
        except Exception as e:
            self.root.after(0, lambda: self.error(str(e)))

    def exito(self):
        self.label_estado.config(text="✅ Reporte generado exitosamente", fg="#27ae60")
        self.btn_generar.config(state="normal")
        ruta_abs = os.path.abspath(RUTA_REPORTE)
        messagebox.showinfo("Listo", f"Tu reporte fue generado exitosamente.\n\nUbicacion:\n{ruta_abs}")
        os.startfile(ruta_abs)

    def error(self, msg):
        self.label_estado.config(text="❌ Error al generar el reporte", fg="red")
        self.btn_generar.config(state="normal")
        messagebox.showerror("Error", f"Ocurrio un error:\n{msg}")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()