from customtkinter import *
from tkinter import filedialog as fd, Menu
from difference import Difference


class App(CTk):
    def __init__(self):
        def _help_info() -> None:
            __alert_info: CTkToplevel = CTkToplevel(self)
            __alert_info.geometry('200x50')
            __alert_info.title('О приложении')
            __alert_info.resizable(width=False, height=False)
            _info_label: CTkLabel = CTkLabel(__alert_info,
                                             text='Version 1.0\n by @jeffrixxxon'
                                            )
            _info_label.pack(side=TOP)

        super().__init__()
        self.geometry('640x420')
        self.resizable(width=False, height=False)
        self.title('Mvideo TDF')
        set_appearance_mode('system')

        # Меню приложения
        self.main_menu: Menu = Menu(self)
        self.config(menu=self.main_menu)
        self.file_menu: Menu = Menu(self.main_menu)
        self.file_menu.add_command(label='Выход', command=self.destroy)
        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)
        self.help_menu: Menu = Menu(self.main_menu)
        self.help_menu.add_command(label='О приложении', command=_help_info)
        self.main_menu.add_cascade(label='Справка', menu=self.help_menu)


class Interface(App):
    def __init__(self):
        super().__init__()
        self.filepath_ts = None
        self.filepath_fact = None
        self.name_colum = None

        # поле системы учета и кнопка открытия файла
        self.entry_ts: CTkEntry = CTkEntry(self,
                                           placeholder_text='Путь к файлу из системы учета',
                                           width=450
                                           )
        self.entry_ts.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)
        self.button_ts: CTkButton = CTkButton(self,
                                              text='Открыть',
                                              command=lambda: self._path_to_file(self.entry_ts)
                                              )
        self.button_ts.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        # поле сроков годности и кнопка открытия файла
        self.entry_fact: CTkEntry = CTkEntry(self,
                                             placeholder_text='Путь к фактическому файлу',
                                             width=450
                                             )
        self.entry_fact.grid(row=2, column=1, padx=10, pady=10, sticky=NSEW)
        self.button_fact: CTkButton = CTkButton(self,
                                                text='Открыть',
                                                command=lambda: self._path_to_file(self.entry_fact)
                                                )
        self.button_fact.grid(row=2, column=2, padx=10, pady=10, sticky=NSEW)

        # поле названия колонки и кнопка "выбрать колонки"
        self.names_colum: CTkOptionMenu = CTkOptionMenu(self,
                                                        values=['Название колонки'],
                                                        state='disabled'
                                                        )
        self.names_colum.grid(row=3, column=1, padx=10, pady=10, sticky=NSEW)
        self.options_menu_button: CTkButton = CTkButton(self,
                                                        text='Выбрать колонку',
                                                        state='disabled',
                                                        command=self._columns_validation
                                                        )
        self.options_menu_button.grid(row=3, column=2, padx=10, pady=10, sticky=NSEW)

        # Кнопка для запуска парсера
        self.start_button: CTkButton = CTkButton(self,
                                                 width=140, height=45,
                                                 text='Запустить',
                                                 state='disabled',
                                                 command=self._button_processing
                                                 )
        self.start_button.grid(row=4, column=2, padx=10, pady=10, sticky='n')

        # лейбл состояния
        self.label_validation: CTkLabel = CTkLabel(self,
                                                   font=('Courier New', 13),
                                                   text='Укажите путь к файлу из системы учета',
                                                   )
        self.label_validation.grid(row=5, column=1, padx=10, pady=10)

        # Поле вывода результата
        self.result_win: CTkTextbox = CTkTextbox(self, width=450, height=200, border_width=2)
        self.result_win.grid(row=4, column=1, padx=10, pady=10, sticky='e')

        # Изменение режима "Ночь/День"
        self.app_mode_status = StringVar(value=get_appearance_mode())
        self.appearance_mode = CTkSwitch(self,
                                         text='Light',
                                         command=self._switch_appearance_mode,
                                         variable=self.app_mode_status,
                                         onvalue="dark", offvalue="light"
                                         )
        self.appearance_mode.grid(row=5, column=2)

    def _switch_appearance_mode(self):
        __mode = self.app_mode_status.get().lower()
        if __mode == 'light':
            self.appearance_mode.configure(text='Dark')
            set_appearance_mode(__mode)
        if __mode == 'dark':
            self.appearance_mode.configure(text='Light')
            set_appearance_mode(__mode)

    def _path_to_file(self, field):
        _file_path: fd = fd.askopenfilename()
        if _file_path != '' and _file_path.split('.')[-1] == 'xlsx':

            with open(_file_path, 'r') as file:
                path: str = file.name
                field.delete(0, END)
                field.insert(0, path)
                if field is self.entry_ts:
                    self.filepath_ts: str = path
                    self.label_validation.configure(text='Укажите путь к фактическому файлу',
                                                    text_color='white')
                if field is self.entry_fact:
                    self.filepath_fact: str = path
                if self.filepath_ts and self.filepath_fact:
                    self.names_colum.configure(state='enabled')
                    self.options_menu_button.configure(state='enabled')
                    self.label_validation.configure(text='Выберете колонку и нажмите кнопку "Выбрать колонку"',
                                                    text_color='white')
                    self.diff: Difference = Difference(self.filepath_ts, self.filepath_fact)
                    self.names_colum.configure(values=self.diff.get_list_columns())
        else:
            field.delete(0, END)
            field.insert(0, 'Неверный формат файла')

    def _button_processing(self):
        if self.filepath_ts and not self.filepath_fact:
            self.label_validation.configure(text='Укажите путь к фактическому файлу',
                                            text_color='white')
        elif not self.filepath_ts and self.filepath_fact:
            self.label_validation.configure(text='Укажите путь к файлу из системы учета',
                                            text_color='white')
        elif self.filepath_ts and self.filepath_fact and self.name_colum:
            _result_diff: list | bool = self.diff.find_difference_numeric(name_column=self.name_colum)
            if _result_diff:
                self.result_win.delete(0.0, END)
                for val in _result_diff:
                    self.result_win.insert(0.0, f'{val}\n')
                self.label_validation.configure(text='Успешно', text_color='green')
            else:
                self.label_validation.configure(text=f'Колонка "{self.name_colum}" отсутствует в фактическом файле',
                                                text_color='red')

    def _columns_validation(self):
        _is_correct_options: set | ValueError = self.diff.column_is_correct()
        self.name_colum = self.names_colum.get()
        self.label_validation.configure(text=f'Колонка {self.name_colum} успешно выбрана\nНажмите кнопку "Запустить"',
                                        text_color='white')
        self.start_button.configure(state='enabled')


def main():
    root: Interface = Interface()
    root.mainloop()


if __name__ == '__main__':
    main()




