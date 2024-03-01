import tkinter
import datetime
from tkinter import Frame, StringVar
from tkinter.ttk import Button, Notebook, Style
from tkinter.ttk import Combobox, Separator
from core.normalizers import TottusNormalizer, TaiLoyNormalizer, RipleyNormalizer, OechsleNormalizer, SagaNormalizer, EstilosNormalizer 
from core.updater import Updater
from util.whateveryouchooser import Chooser
from pathlib import Path
from tkinter import messagebox
import os
from config import ICON_PATH


class MainWindow(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("430x300")

        self.tottus_normalizer = TottusNormalizer()
        self.oechsle_normalizer = OechsleNormalizer()
        self.ripley_normalizer = RipleyNormalizer()
        self.tailoy_normalizer = TaiLoyNormalizer()
        self.estilos_normalizer = EstilosNormalizer()
        self.saga_normalizer = SagaNormalizer()

        # This line only works in Windows :(
        try:
            self.iconbitmap(ICON_PATH)
        except Exception as e:
            print("No se puedo cargar la imagen")

        # This line only works in Linux
        # try:
        #     self.iconphoto(False, tkinter.PhotoImage(ICON_PATH))
        # except Exception as e:
        #     print("No se puedo cargar la imagen")

        self.title("Updater")

        nb = Notebook()

        nb.add(self.__create_tottus_frame__(nb), text="TOTTUS")
        nb.add(self.__create_ripley_frame__(nb), text="RIPLEY")
        nb.add(self.__create_oechsle_frame__(nb), text="OECHSLE")
        nb.add(self.__create_tailoy_frame__(nb), text="TAI LOY")
        nb.add(self.__create_estilos_frame__(nb), text="ESTILOS")
        nb.add(self.__create_saga_frame__(nb), text="SAGA FALABELLA")

        nb.pack(fill='both', expand='yes')

    def __create_tottus_frame__(self, parent):
        frame_tottus = Frame(parent)
        sells_function = lambda: self.create_output_ventas(self.tottus_normalizer)
        stock_function = lambda: self.create_output_stock(self.tottus_normalizer)

        sells_button = Button(frame_tottus, text="GENERAR VENTAS", command=sells_function, width=40)
        stock_button = Button(frame_tottus, text="GENERAR STOCK", command=stock_function, width=40)

        sells_button.pack(padx=5, pady=5)
        stock_button.pack(padx=5, pady=5)
        return frame_tottus
    
    def __create_ripley_frame__(self, parent):
        frame_ripley = Frame(parent)
        sells_function = lambda: self.create_output_ventas(self.ripley_normalizer)
        stock_function = lambda: self.create_output_stock(self.ripley_normalizer)

        sells_button = Button(frame_ripley, text="GENERAR VENTAS", command=sells_function, width=40)
        sells_stock = Button(frame_ripley, text="GENERAR STOCK", command=stock_function, width=40)
        oc_button = Button(frame_ripley, text="NORMALIZAR OC")

        sells_button.pack(padx=7, pady=7)
        sells_stock.pack(padx=7, pady=7)
        oc_button.pack(padx=7, pady=7)
        return frame_ripley
    
    def __create_oechsle_frame__(self, parent):
        oechsle_frame = Frame(parent)
        return oechsle_frame

    def __create_tailoy_frame__(self, parent):
        style = Style().configure("TButton", padding=6, relief="flat",
            background="#ccc")
        tailoy_frame = Frame(parent)
        sells_function = lambda: self.create_output_ventas(self.tailoy_normalizer)
        sells_button = Button(tailoy_frame, text="GENERAR VENTAS", command=sells_function, width=40)
        sells_button.pack(padx=5, pady=5)
        stock_function = lambda: self.create_output_stock(self.tailoy_normalizer)
        stock_button = Button(tailoy_frame, text="GENERAR STOCK", command=stock_function, width=40)
        stock_button.pack(padx=7, pady=7)
        return tailoy_frame
    
    def __create_estilos_frame__(self, parent):
        estilos_frame = Frame(parent)
        sells_function = lambda: self.create_output_ventas(self.estilos_normalizer)
        stock_funciont = lambda: self.create_output_stock(self.estilos_normalizer)
     
        sells_button = Button(estilos_frame, text="GENERAR VENTAS", command=sells_function, width=40)
        stock_button = Button(estilos_frame, text="GENERAR STOCK", command=stock_funciont, width=40)

        sells_button.pack(padx=7, pady=7)
        stock_button.pack(padx=7, pady=7)

        return estilos_frame
    
    def __create_saga_frame__(self, parent):
        def on_combobox_change(event):
            # Acceder al valor seleccionado en el Combobox
            self.saga_normalizer.year = year.get()
            # Mostrar el valor seleccionado en la etiqueta

        saga_frame = Frame(parent)
        current_year = datetime.datetime.now().year
        year = tkinter.IntVar(value=current_year)
        SagaNormalizer.year = year.get()
        combobox = Combobox(saga_frame, values=[year for year in range(current_year, 1999, -1)], state='readonly', textvariable=year, width=45)
        combobox.bind("<<ComboboxSelected>>", on_combobox_change)
        sells_function = lambda: self.create_output_ventas(self.saga_normalizer)
        sells_button = Button(saga_frame, text="GENERAR VENTAS", command=sells_function, width=40)
        combobox.pack(padx=7, pady=7)
        sells_button.pack(padx=7, pady=7)

        stock_function = lambda: self.create_output_stock(self.saga_normalizer)
        stock_button = Button(saga_frame, text="GENERAR STOCK", width=40, command=stock_function)
        stock_button.pack(padx=7, pady=7)

        return saga_frame

    def __open_excel__(self, path):
        os.startfile(path)

        
    def create_output_ventas(self, normalizer):
        try:
            path = self.__select_directory__()
            if not path:
                return
            updater = Updater()
            filename = f"OUTPUT-{normalizer}.xlsx"
            path = updater.consolidate_sells(path, normalizer, filename)
            print("Ventas creado con exito")
            response = messagebox.askyesno("Terminado", f"Archivo {path.name} creado con éxito ¿Abrir?")
            if response:
                self.__open_excel__(path)
        except Exception as e:
            messagebox.showerror(message="Algo fue mal")

    def create_output_stock(self, normalizer):
        try:
            path = self.__select_file__()
            if not path:
                return
            updater = Updater()
            filename = f"STOCK-OUTPUT-{normalizer}.xlsx"
            path = updater.create_stock(path, normalizer, filename)
            print("Stock creado con exito")
            response = messagebox.askyesno("Terminado", f"Archivo {path.name} creado con éxito ¿Abrir?")
            if response:
                self.__open_excel__(path)
        except Exception as e:
            messagebox.showerror(message="Algo fue mal")
            

    
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

root = MainWindow()
root.mainloop() # app

