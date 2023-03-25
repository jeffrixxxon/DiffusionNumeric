import os
import typing
import pandas as pd
import time


class NotificationError(Exception):
    pass


def conv_xlsx_to_csv(name_file_xlsx_1: str, name_file_xlsx_2, cols_search) -> typing.NoReturn:
    try:
        dfs_1 = pd.read_excel(f"files/{name_file_xlsx_1}.xlsx", usecols=[cols_search])
        dfs_2 = pd.read_excel(f"files/{name_file_xlsx_2}.xlsx", usecols=[cols_search])
    except NotificationError as err:
        print("[-]Столбец не найден!")
        raise err
    dfs_1.to_csv(f'files/{name_file_xlsx_1}.csv')
    dfs_2.to_csv(f'files/{name_file_xlsx_2}.csv')


def numeric_number(name_file_csv: str) -> set:
    result = []
    with open(f'files/{name_file_csv}.csv', encoding='utf-8') as file:
        for line in file.readlines():
            result.append(line.split(',')[1].lstrip('.'))
    return set(map(lambda x: f"{x.split('.')[0]}\n", result[1:]))


def create_result_txt(name_csv_1: str, name_csv_2: str) -> typing.NoReturn:
    with open('files/result.txt', 'w', encoding='utf-8') as file:
        file.writelines(numeric_number(name_csv_1).difference(numeric_number(name_csv_2)))
    try:
        os.remove(f'files/{name_csv_1}.csv')
        os.remove(f'files/{name_csv_2}.csv')
    except FileNotFoundError:
        pass #TOODO


def main():
    try:
        file_xlsx_1 = input('[+]Введите имя файла из TS №1: ')
        file_xlsx_2 = input('[+]Введите имя отслеживаемого файла №2: ')
        cols = input('[+]Введите название столбца для поиска для поиска: ')
        conv_xlsx_to_csv(file_xlsx_1, file_xlsx_2, cols)
    except FileNotFoundError:
        print('[-]Введенный файл не найден. Попробуйте снова.')
        main()

    create_result_txt(file_xlsx_1, file_xlsx_2)

    print('[+]Success')

    print('[+]Очистить папку /files?: [Y/N]')
    request = input()
    if request.upper() == 'Y':
        os.remove(f'files/{file_xlsx_1}.xlsx')
        os.remove(f'files/{file_xlsx_2}.xlsx')


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print(time.perf_counter() - start)



