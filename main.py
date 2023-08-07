import sentry_sdk
from customtkinter import *
from tkinter import filedialog as fd, Menu, messagebox
from difference import Difference

sentry_sdk.init(
    dsn="https://fd100801f7da46c8869489648dd9ddca@o4505170256855040.ingest.sentry.io/4505170304827392",
    traces_sample_rate=1.0
)


class App(CTk):
    def __init__(self):
        def _help_info() -> None:
            __msg = 'Version 0.2\nBy @jeffrixxxon'
            messagebox.showinfo('About', message=__msg)

        super().__init__()
        self.geometry('640x430')
        self.resizable(width=False, height=False)
        self.title('TDF')
        self.iconbitmap('icon.ico')
        set_appearance_mode('light')

        # Create a menu bar
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # Create a file menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Create a help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=_help_info)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)


class Interface(App):
    def __init__(self):
        super().__init__()
        self.filepath_ts: str = ''
        self.filepath_fact: str = ''
        self.name_colum: str = ''

        self.entry_ts: CTkEntry = CTkEntry(self,
                                           placeholder_text='Путь к файлу из системы учета',
                                           width=450
                                           )
        self.entry_ts.grid(row=0, column=1, padx=10, pady=10)
        self.button_ts: CTkButton = CTkButton(self,
                                              text='Открыть',
                                              command=lambda: self._path_to_file(self.entry_ts)
                                              )
        self.button_ts.grid(row=0, column=2, padx=10, pady=10)

        self.entry_fact: CTkEntry = CTkEntry(self,
                                             placeholder_text='Путь к фактическому файлу',
                                             width=450
                                             )
        self.entry_fact.grid(row=2, column=1, padx=10, pady=10)
        self.button_fact: CTkButton = CTkButton(self,
                                                text='Открыть',
                                                command=lambda: self._path_to_file(self.entry_fact)
                                                )
        self.button_fact.grid(row=2, column=2, padx=10, pady=10)

        self.names_colum: CTkOptionMenu = CTkOptionMenu(self,
                                                        values=['Название колонки'],
                                                        state='disabled',
                                                        width=450,
                                                        height=28
                                                        )
        self.names_colum.grid(row=3, column=1, padx=10, pady=0)
        self.options_menu_button: CTkButton = CTkButton(self,
                                                        text='Выбрать колонку',
                                                        state='disabled',
                                                        command=self._columns_validation
                                                        )
        self.options_menu_button.grid(row=3, column=2, padx=10, pady=10)

        self.label_validation: CTkLabel = CTkLabel(self,
                                                   font=('Courier New', 13),
                                                   text='Укажите путь к файлу из системы учета',
                                                   )
        self.label_validation.grid(row=4, column=1, padx=10, pady=1)

        self.start_button: CTkButton = CTkButton(self,
                                                 width=140, height=40,
                                                 text='Запустить',
                                                 state='disabled',
                                                 command=self._button_processing
                                                 )
        self.start_button.grid(row=4, column=2, padx=10, pady=1, sticky='n')

        self.result_win: CTkTextbox = CTkTextbox(self, width=450, height=200, border_width=2)
        self.result_win.grid(row=5, column=1, padx=10, pady=2, sticky=NSEW)

    def _path_to_file(self, field):
        _file_path: fd = fd.askopenfilename() # TODO
        if _file_path != '' and _file_path.split('.')[-1] == 'xlsx':

            with open(_file_path, 'r') as file:
                _path: str = file.name
                field.delete(0, END)
                field.insert(0, _path)
                if field is self.entry_ts:
                    self.filepath_ts: str = _path
                    self.label_validation.configure(text='Укажите путь к фактическому файлу',
                                                    text_color='white')
                if field is self.entry_fact:
                    self.filepath_fact: str = _path
                if self.filepath_ts and self.filepath_fact:
                    self.names_colum.configure(state='enabled')
                    self.options_menu_button.configure(state='enabled')
                    self.label_validation.configure(text='Выберете колонку и нажмите кнопку "Выбрать колонку"',
                                                    text_color='white')
                    self.diff: Difference = Difference(self.filepath_ts, self.filepath_fact)
                    self.list_column = self.diff.get_list_columns()
                    if self.list_column == 'TradeError':
                        self.label_validation.configure(text='Файл системы учета пуст', text_color='red')
                    elif self.list_column == 'FactFileError':
                        self.label_validation.configure(text='Фактический файл пуст', text_color='red')
                    else:
                        self.names_colum.configure(values=self.list_column)

        else:
            field.delete(0, END)
            field.insert(0, 'Неверный формат файла')

    def _save_us(self):
        with fd.asksaveasfile(title='Сохранить как', defaultextension=".txt") as new_file:
            if new_file:
                new_file.writelines(self.result_diff)

    def _button_processing(self):
        if self.filepath_ts and not self.filepath_fact:
            self.label_validation.configure(text='Укажите путь к фактическому файлу',
                                            text_color='white')
        elif not self.filepath_ts and self.filepath_fact:
            self.label_validation.configure(text='Укажите путь к файлу из системы учета',
                                            text_color='white')
        elif self.filepath_ts and self.filepath_fact and self.name_colum:
            self.result_diff: list | bool = self.diff.find_difference_numeric(name_column=self.name_colum)
            if self.result_diff:
                self.result_win.delete(0.0, END)
                self.result_win.insert(0.0, self.result_diff)
                self.label_validation.configure(text='Успешно', text_color='green')
            else:
                self.label_validation.configure(text=f'Колонка "{self.name_colum}" отсутствует в фактическом файле',
                                                text_color='red')

    def _columns_validation(self):
        _is_correct_options: set | ValueError = self.diff.column_is_correct()
        if isinstance(_is_correct_options, set):
            self.name_colum = self.names_colum.get()
            self.label_validation.configure(text=f'Колонка {self.name_colum} успешно выбрана\nНажмите кнопку "Запустить"',
                                            text_color='white')
            self.start_button.configure(state='enabled')
        else:
            self.label_validation.configure(text=f'Произошла ошибка: {_is_correct_options}')


def main():
    root: Interface = Interface()
    root.mainloop()


if __name__ == '__main__':
    main()




