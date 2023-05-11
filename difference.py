import os
import pandas as pd


class Difference:
    def __init__(self, path_ts: str, path_fact: str):
        self.data_frame_ts: pd.DataFrame = pd.DataFrame()
        self.data_frame_fact: pd.DataFrame = pd.DataFrame()
        self.ts: str = path_ts
        self.fact: str = path_fact

    def get_list_columns(self) -> list:
        try:
            self.data_frame_ts = pd.read_excel(self.ts)
            self.data_frame_fact = pd.read_excel(self.fact)
            return self.data_frame_ts.columns.tolist()
        except Exception as err:
            return err.__class__

    def find_difference_numeric(self, name_column: str) -> list:
        try:
            _trade: pd.DataFrame = self.data_frame_ts[name_column].dropna(how='all')
            _fact: pd.DataFrame = self.data_frame_fact[name_column].dropna(how='all')
            _result_difference_num: set = set(_trade.tolist()
                                              ).difference(set(_fact.tolist()))
            return list(map(str, _result_difference_num))
        except KeyError:
            return False

    def column_is_correct(self):
        try:
            _correct_ts: list = self.data_frame_ts.columns.tolist()
            _correct_fact: list = self.data_frame_fact.columns.tolist()
            _difference_ts_in_fact: set = set(_correct_ts).difference(_correct_fact)
            return _difference_ts_in_fact
        except ValueError as err:
            return err.__class__


if __name__ == '__main__':
    path_2 = '/Users/daniil/Downloads/Сроки годности.xlsx'
    path_1 = '/Users/daniil/Downloads/trade.xlsx'
    if os.path.exists(path_1) and os.path.exists(path_2):
        diff = Difference(path_1, path_2)
        print(diff.get_list_columns())

