from customtkinter import *
from tkinter import filedialog as fd
from difference import Difference


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('640x480')
        self.title('Mvideo TDF')
        set_appearance_mode('system')


class Interface(App):
    def __init__(self):
        super().__init__()
        self.filepath_ts = None
        self.filepath_fact = None
        self.name_colum = None
        # поле системы учета и кнопка
        self.entry_ts = CTkEntry(self, placeholder_text='Путь к файлу из системы учета', width=450)
        self.entry_ts.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)
        self.button_ts = CTkButton(self, text='Открыть', command=lambda: self._path_to_file(self.entry_ts))
        self.button_ts.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)
        # поле сроков годности и кнопка
        self.entry_fact = CTkEntry(self, placeholder_text='Путь к фактическому файлу')
        self.entry_fact.grid(row=2, column=1, padx=10, pady=10, sticky=NSEW)
        self.button_fact = CTkButton(self, text='Открыть', command=lambda: self._path_to_file(self.entry_fact))
        self.button_fact.grid(row=2, column=2, padx=10, pady=10, sticky=NSEW)
        # поле названия колонки и кнопка "выбрать колонки"
        self.names_colum = CTkOptionMenu(self, values=['Название колонки'], state='disabled')
        self.names_colum.grid(row=3, column=1, padx=10, pady=10, sticky=NSEW)
        self.options_menu_button = CTkButton(self, text='Выбрать колонку', state='disabled', command=self._columns_validation)
        self.options_menu_button.grid(row=3, column=2, padx=10, pady=10, sticky=NSEW)
        # Кнопка для запуска парсера
        self.start_button = CTkButton(self, height=45, text='Запустить', state='disabled', command=self._button_processing)
        self.start_button.grid(row=4, column=1, padx=10, pady=10, sticky=NSEW)
        # лейбл состояния
        self.label_frame = CTkFrame(self, width=300, height=100)
        self.label_frame.grid(row=5, column=1, padx=10, pady=10)
        self.label_validation = CTkLabel(self.label_frame, text='Укажите путь к файлу из системы учета')
        self.label_validation.grid(row=5, column=1, padx=10, pady=10, sticky=NSEW)

    def _path_to_file(self, field):
        _file_path = fd.askopenfilename()
        if _file_path != '' and _file_path.split('.')[-1] == 'xlsx':

            with open(_file_path, 'r') as file:
                path = file.name
                field.delete(0, END)
                field.insert(0, path)
                if field is self.entry_ts:
                    self.filepath_ts = path
                    self.label_validation.configure(text='Укажите путь к фактическому файлу')
                if field is self.entry_fact:
                    self.filepath_fact = path
                if self.filepath_ts and self.filepath_fact:
                    self.names_colum.configure(state='enabled')
                    self.options_menu_button.configure(state='enabled')
                    self.label_validation.configure(text='Выберете колонку и нажмите кнопку "Выбрать колонку"')
                    self.diff = Difference(self.filepath_ts, self.filepath_fact)
                    self.names_colum.configure(values=self.diff.get_list_columns())
        else:
            field.delete(0, END)
            field.insert(0, 'Неверный формат файла')

    def _button_processing(self):
        if self.filepath_ts and not self.filepath_fact:
            self.label_validation.configure(text='Укажите путь к фактическому файлу')
        elif not self.filepath_ts and self.filepath_fact:
            self.label_validation.configure(text='Укажите путь к файлу из системы учета')
        elif self.filepath_ts and self.filepath_fact and self.name_colum:
            _result_diff = self.diff.find_difference_numeric(name_column=self.name_colum)
            self.label_validation.configure(text=_result_diff)

    def _columns_validation(self):
        _is_correct_options = self.diff.column_is_correct()
        self.name_colum = self.names_colum.get()
        self.label_validation.configure(text=f'Колонка {self.name_colum} успешно выбрана\nНажмите кнопку "Запустить"')
        self.start_button.configure(state='enabled')


def main():
    root: Interface = Interface()
    root.mainloop()


if __name__ == '__main__':
    main()




