from customtkinter import *
from tkinter import filedialog as fd
from difference import Difference


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('640x480')
        self.title('Mvideo TDF')
        set_appearance_mode('system')
        self.entry_ts = CTkEntry(self, placeholder_text='Путь к файлу  TS', width=400)
        self.entry_ts.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)
        self.button_ts = CTkButton(self, text='Открыть', command=self.ts_file_name)
        self.button_ts.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)
        self.entry_fact = CTkEntry(self, placeholder_text='Путь к фактическому файлу')
        self.entry_fact.grid(row=2, column=1, padx=10, pady=10, sticky=NSEW)
        self.button_fact = CTkButton(self, text='Открыть', command=self.fact_file_name)
        self.button_fact.grid(row=2, column=2, padx=10, pady=10, sticky=NSEW)
        self.name_colum = CTkEntry(self, placeholder_text='Название колонки')
        self.name_colum.grid(row=3, column=1, padx=10, pady=10, sticky=NSEW)

    def ts_file_name(self):
        filepath_ts = fd.askopenfilename()
        if filepath_ts != '' and filepath_ts.split('.')[-1] == 'xlsx':
            with open(filepath_ts, 'r') as file:
                text = file.name
                self.entry_ts.delete(0, END)
                self.entry_ts.insert(0, text)
        else:
            self.entry_ts.delete(0, END)
            self.entry_ts.insert(0, 'Неверный формат файла.')

    def fact_file_name(self):
        filepath_fact = fd.askopenfilename()
        if filepath_fact != '' and filepath_fact.split('.')[-1] == 'xlsx':
            with open(filepath_fact, 'r') as file:
                text = file.name
                self.entry_fact.delete(0, END)
                self.entry_fact.insert(0, text)
        else:
            self.entry_ts.delete(0, END)
            self.entry_ts.insert(0, 'Неверный формат файла.')


def main():
    root = App()
    root.mainloop()


if __name__ == '__main__':
    main()




