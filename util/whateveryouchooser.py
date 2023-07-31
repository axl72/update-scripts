from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfile, asksaveasfilename
import os


class Chooser:

    def __init__(self):
        self.directory_selected = None
        self.file_selected = None
        self.initialdir = escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    
    def __select_archive__(self, chooser, **options):
        root = Tk()
        root.withdraw()
        root.update()
        pathString = chooser()
        root.destroy()
        self.directory_selected = pathString
        return pathString

    def select_directory(self):
        directory_selected = askdirectory(initialdir=self.initialdir)
        return directory_selected
        
    
    def select_file(self):
        file_selected = askopenfilename(initialdir=self.initialdir)
        return file_selected
    
    def save_file(self):
        asksaveasfile(initialdir=self.initialdir)
    
    def get_last_directorypath(self):
        return self.directory_selected
    
    def get_last_filepath(self):
        return self.file_selected