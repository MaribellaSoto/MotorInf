import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile

class Application(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        tk.Label(master, text="Inteligencia Artificial ", bg='Pink',font=('Times New Roman', 30)).place(x=180, y=10)
        tk.Label(master, text="Maribella Soto Larios-María Guadalupe Torres Amezcua", bg='Pink', font=(None, 12)).place(x=170, y=60)
        self.btnSeleccionar = tk.Button(master, text="Cargar entradas (archivo)", font=('Times New Roman', 11), command=self.openArchive, width=35)
        self.btnSeleccionar.place(x=230, y=100)
        tk.Label(master, text="Reglas", bg='Pink', font=('Times New Roman', 16)).place(x=10, y=150)
        self.reglas = tk.Text(master, font=(None, 12), width=40, height=10)
        self.reglas.place(x=10, y=180)
        tk.Label(master, text="Seleccione el tipo de encadenamiento: ", bg='Pink', font=('Times New Roman', 12)).place(x=380, y=180)
        self.lista = ttk.Combobox(master, state="readonly", values=["", "Encadenamiento hacia adelante", "Encadenamiento hacia atrás"], font=(None, 12))
        self.lista.place(x=380, y=200)
        tk.Label(master, text="Hechos iniciales(BH): ", font=('Times New Roman', 12), bg="Pink").place(x=380, y=225)
        self.bh = ttk.Entry(master, font=(None, 12))    
        self.bh.place(x=380, y=250)
        tk.Label(master, text="Objetivo meta: ", font=('Times New Roman', 12), bg="Pink").place(x=380, y=275)
        self.meta = ttk.Entry(master, font=(None, 12))
        self.meta.place(x=380, y=300)
        self.btnCalcular = tk.Button(master, text="Procesar", font=('Times New Roman', 12), command=self.iniciarProceso, width=15)
        self.btnCalcular.place(x=90, y=380)
        self.btnReiniciar = tk.Button(master, text="Reiniciar", font=('Times New Roman', 12), command=self.reiniciar, width=15)
        self.btnReiniciar.place(x=500, y=380)
        tk.Label(master, text="Proceso", bg='Pink', font=('Times New Roman', 16)).place(x=10, y=420)
        #crear tabla para resultados
        self.tablita = ttk.Treeview(master)
        self.tablita["columns"] = ("1", "2", "3", "4")
        self.tablita.heading("#0", text="cc")
        self.tablita.column("#0",minwidth=0,width=240)
        self.tablita.heading("1", text="nh-nm")
        self.tablita.column("#1",minwidth=0,width=80)
        self.tablita.heading("2", text="meta")
        self.tablita.column("#2",minwidth=0,width=80)
        self.tablita.heading("3", text="r")
        self.tablita.column("#3",minwidth=0,width=80)
        self.tablita.heading("4", text="bh")
        self.tablita.column("#4",minwidth=0,width=240)
        self.tablita.place(x=10, y=450)
        master.title("Actividad 2. Motor de inferencia")
        master.configure(bg='Pink')
        self.place(x=510, y=750)

    def openArchive(self):
        filename = askopenfile()
        with open(filename.name, 'r') as file:
            cadena = file.readline()
            while cadena != "":
                self.reglas.insert(tk.END, cadena)
                cadena = file.readline()
        self.filename = filename.name

    def iniciarProceso(self):
        BH = list(self.bh.get().split(","))
        meta = self.meta.get().upper()
        bc = self.obtenerBC()
        corrector = {}
        cc = []
        self.tablita.insert("", tk.END, text="{}", values=("", meta, "", BH))
        if self.lista.get() == "Encadenamiento hacia adelante":
            while len(bc) > 0 and meta not in BH:
                corrector.clear()
                for i in bc.values():
                    leng = len(i[0]) - len(i[0]) // 2
                    cont = 0
                    for w in BH:
                        if w.upper() in i[0]:
                            cont += 1
                    if cont == leng:
                        cc.append(list(bc.keys())[list(bc.values()).index(i)])
                if len(cc) > 0:
                    cc = [corrector.setdefault(x, x) for x in cc if x not in corrector]
                    nh = bc[cc[0]][2]
                    BH.append(nh)
                    self.tablita.insert("", tk.END, text=cc, values=(nh, meta, cc[0], BH))
                    bc.pop(cc[0])
                    cc.pop(0)
                else:
                    break
            if meta in BH:
                messagebox.showinfo(
                    message=f"ÉXITO",
                    title="Resultado"
                )
            else:
                messagebox.showinfo(
                    message=f"FRACASO",
                    title="Resultado"
                )
        elif self.lista.get() == "Encadenamiento hacia atrás":
            if self.verificar(meta, BH, [meta]):
                messagebox.showinfo(
                    message=f"ÉXITO",
                    title="Resultado"
                )
            else:
                messagebox.showinfo(
                    message=f"FRACASO",
                    title="Resultado"
                )

    def obtenerBC(self):
        reglas = {}
        with open(self.filename, 'r') as file:
            regla = list(file.readline().split(sep=" "))
            while regla != [""]:
                reglas.setdefault(regla[0], regla[1:])
                regla = list(file.readline().split(sep=" "))
        for i in reglas.keys():
            reglas[i][-1] = reglas[i][-1].replace("\n", "")
            print(reglas[i][-1])
        return reglas

    def verificar(self, meta, BH, nm) -> bool:
        bc = self.obtenerBC()
        cont = 0
        cc = []
        nm = nm
        verificado = False
        if meta in BH:
            return True
        else:
            for i in bc.values():
                if meta == i[-1]:
                    cc.append(list(bc.keys())[list(bc.values()).index(i)])
            while cc != [] and not verificado:
                r = cc.pop()
                long = len(bc[r][0].split(","))
                for i in bc.get(r):
                    if i in BH:
                        cont +=1
                nm.extend(bc[r][0].split(","))
                for i in nm:
                    if i in BH:
                        del nm[nm.index(i)]
                verificado = True
                while nm != [] and verificado:
                    meta = nm[0]
                    if cont == long:
                        BH.insert(0, meta)
                    nm.pop(0)
                    verificado = self.verificar(meta, BH, nm)

                    if verificado:
                        BH.insert(0, meta)
                    lista = []
                    for i in range(len(BH)-1, -1, -1):
                        if BH[i] not in lista:
                            lista.insert(0, BH[i])
                    BH = lista
                    self.tablita.insert("", tk.END, text=r, values=(nm, meta, r, BH))
            return verificado

    def reiniciar(self):
        self.bh.delete(0, tk.END)
        self.meta.delete(0, tk.END)
        self.reglas.delete(1.0, tk.END)
        self.tablita.delete(*self.tablita.get_children())
        self.lista.current(0)

frame = tk.Tk()
frame.resizable(0,0)
window_height = 700
window_width = 750
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
frame.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
app = Application(frame)
app.pack()
app.mainloop()
