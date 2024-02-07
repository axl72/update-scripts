import tkinter
from tkinter import Button, Frame, StringVar
from tkinter.ttk import Combobox, Separator
from core.normalizers import TottusNormalizer, TaiLoyNormalizer, RipleyNormalizer, OechsleNormalizer, SagaNormalizer, EstilosNormalizer 
from core.updater import Updater
from util.whateveryouchooser import Chooser
from pathlib import Path
from tkinter import messagebox
import os

normalizers = (TottusNormalizer(), RipleyNormalizer(), OechsleNormalizer(), TaiLoyNormalizer(), EstilosNormalizer(), SagaNormalizer())

class MainWindow(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("230x300")
        self.iconbitmap("C:\\Users\\USUARIO\\Desktop\\ENTORNO\\perro-tejonero.ico")
        self.title("Updater")
        self.frame = Frame(self)
        self.values = ["TOTTUS", "RIPLEY", "OECHSLE", "TAI LOY", "ESTILOS", "SAGA FALABELLA"]
        self.cliente_seleccionado = StringVar()
        self.combobox_cliente = Combobox(self.frame, values=self.values, textvariable=self.cliente_seleccionado)

        self.combobox_cliente.bind("<<ComboboxSelected>>", self.on_combobox_change)
        # self.combobox_tipo = Combobox(self.frame)
        self.boton_ventas = Button(self.frame, text="VENTAS", command=self.create_output_ventas)
        self.boton_stock = Button(self.frame, text="INVENTARIO", command=self.create_output_stock)
        self.sep = Separator(self)

        self.combobox_cliente.pack(side="top", padx=5, pady=5)
        self.boton_ventas.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.boton_stock.pack(side="right", padx=5, pady=5, fill="x", expand=True)
        # self.combobox_tipo.pack(side="right", padx=5, pady=5)
        self.frame.pack(side="top")
        self.sep.pack(side="top", fill="x")
        # self.button_1 = self.__add_button__("Tottus", None)
        # self.button_2 = self.__add_button__("Ripley", None)
        # self.button_3 = self.__add_button__("Oechsle", None)
        # self.button_4 = self.__add_button__("Tai Loy", None)
    
    def __add_button__(self, text:str, function):
        button = Button(text=text, command=function, padx=55, pady=10, borderwidth=5)
        button.pack(padx=5, pady=5)
        return button
    
    def __open_excel__(self, path):
        os.startfile(path)

        
    def create_output_ventas(self):
        normalizer = normalizers[self.selected_index]
        path = self.__select_directory__()
        updater = Updater()
        filename = f"OUTPUT-{normalizer}.xlsx"
        path = updater.consolidate_sells(path, normalizer, filename)
        print("Ventas creado con exito")
        response = messagebox.showinfo("Terminado", f"Archivo {path.name} creado con éxito ¿Abrir?")
        if response:
            self.__open_excel__(path)

    def create_output_stock(self):
        normalizer = normalizers[self.selected_index]
        path = self.__select_file__()
        updater = Updater()
        filename = f"STOCK-OUTPUT-{normalizer}.xlsx"
        path = updater.create_stock(path, normalizer, filename)
        print("Stock creado con exito")
        response = messagebox.askyesno("Terminado", f"Archivo {path.name} creado con éxito ¿Abrir?")
        if response:
            self.__open_excel__(path)

    
    def __select_directory__(self) -> Path:
        selected_directory = Chooser().select_directory()
        if selected_directory == "":
            print("Ningun directorio seleccionado")
            return
        directory = Path(selected_directory)
        return directory
    
    def __select_file__(self) -> Path:
        selected_file = Chooser().select_file()
        if selected_file == "":
            print("Ningun archivo seleccionado")
            return
        file = Path(selected_file)
        return file
    def on_combobox_change(self, event):
        self.selected_index = self.combobox_cliente.current()
        self.cliente_seleccionado.set(normalizers[self.selected_index])
        print(f"Cliente seleccionado {self.cliente_seleccionado}")

root = MainWindow()
root.mainloop() # app

