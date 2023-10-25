import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
# from analizador import analizar
# from analizador import genera_reporte, analizar, errores_en
import sys
import os


class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#232526",
            foreground="#e8e8e8",
            insertbackground="#444546",
            selectbackground="#5b5d5d",
            width=52,
            height=25,
            font=("Courier New", 11),
        )

        self.scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=35, bg="#2c2e2f")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()



class ScrollTextConsola(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#232526",
            foreground="#e8e8e8",
            insertbackground="#444546",
            selectbackground="#5b5d5d",
            width=27,
            height=25,
            font=("Courier New", 11),
        )

        self.scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=35, bg="#2c2e2f")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="#e8e8e8",
                font=("Courier New", 11, "bold"),
            )
            i = self.textwidget.index("%s+1line" % i)


class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto 1")
        self.geometry("850x530")
        self.config(background="#f0f0f0")
        self.centrar(self, 850, 530)
        self.resizable(0, 0)
        self.overrideredirect(True)
    
        # visualizar bizdata, editar datos
        self.scroll = ScrollText(self)
        self.scroll.place(x=5, y=45)
        self.after(200, self.scroll.redraw())

        # visualizador de consola
        self.scroll_consola = ScrollTextConsola(self)
        self.scroll_consola.place(x=535, y=45)
        self.after(200, self.scroll_consola.redraw())

        # genera html: reporte de tokens, reporte de errores, arbol de derivacion
        btn_reporte_tokens = Button(self, text="Reporte de tokens", command=self.reporte_tokens,
                             width=20, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_reporte_tokens.place(x=160, y=10)

        btn_reporte_errores = Button(self, text="Reporte de errores", command=self.reporte_errores,
                              width=20, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_reporte_errores.place(x=340, y=10)

        btn_arbol = Button(self, text="Arbol de derivacion", command=self.reporte_arbol,
                                 width=20, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_arbol.place(x=520, y=10)

        # labels consola
        self.lbl_consola = Label(self, text="[ consola >>> ]", bg=(
            "#f0f0f0"), fg=("#ababac"), font=("Lucida Sans", 10))
        self.lbl_consola.place(x=650, y=474)

        # menu buttons: abrir, analizar, inicializar, salir
        btn_abrir = Button(self, text="Abrir", command=self.abrir_archivo,
                             width=10, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_abrir.place(x=220, y=490)

        btn_analizar = Button(self, text="Analizar", command=self.analizar_json,
                              width=10, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_analizar.place(x=320, y=490)

        btn_inicializar = Button(self, text="Inicializar", command=self.inicializar,
                                 width=10, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_inicializar.place(x=420, y=490)

        btn_salir = Button(self, text="Salir", command=self.quit,
                              width=10, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_salir.place(x=520, y=490)

    def centrar(self, ventana, ancho, alto):  # centra la ventana
        altura_pantalla = ventana.winfo_screenheight()
        ancho_pantalla = ventana.winfo_screenwidth()
        ancho_x = (ancho_pantalla//2) - (ancho//2)
        altura_y = (altura_pantalla//2) - (alto//2)
        ventana.geometry(f"+{ancho_x}+{altura_y}")

    def abrir_archivo(self):
        filepath = askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        self.scroll.delete(1.0, tk.END)  # Limpia el área de texto
        with open(filepath, "r") as input_file:
            text = input_file.read()
            # Inserta la información del archivo seleccionado
            self.scroll.insert(tk.END, text)
        self.title(f"Proyecto 1 - {filepath}")

    def analizar_json(self):
        print("Analizando...")

    def inicializar(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def reporte_tokens(self):
        print("generando html tokens...")

    def reporte_errores(self):
        print("generando html errores...")
    
    def reporte_arbol(self):
        print("generando html arbol...")


app = Ventana()
app.mainloop()
