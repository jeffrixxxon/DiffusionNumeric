import os
import pandas as pd


class Difference:
    def __init__(self, path_ts: str, path_fact: str):
        self.new_frame: pd.DataFrame = pd.DataFrame()
        self.data_frame_ts: pd.DataFrame = pd.DataFrame()
        self.data_frame_fact: pd.DataFrame = pd.DataFrame()
        self.ts: str = path_ts
        self.fact: str = path_fact

    def get_list_columns(self) -> list:
        self.data_frame_ts = pd.read_excel(self.ts)
        self.data_frame_fact = pd.read_excel(self.fact)
        return self.data_frame_ts.columns.tolist()

    def find_difference_numeric(self, name_column: str) -> list:
        _trade: list = self.data_frame_ts[name_column].tolist()
        _fact: list = self.data_frame_fact[name_column].tolist()
        _result_difference_num: set = set(_trade).difference(set(_fact))
        return list(map(str, _result_difference_num))

    def column_is_correct(self):
        if self.data_frame_fact and self.data_frame_ts:
            _correct_ts = self.data_frame_ts.columns.tolist()
            _correct_fact = self.data_frame_fact.columns.tolist()
            return set(_correct_ts).difference_update(_correct_fact)


if __name__ == '__main__':
    path_2 = '/Users/daniil/Downloads/Сроки годности.xlsx'
    path_1 = '/Users/daniil/Downloads/trade.xlsx'
    if os.path.exists(path_1) and os.path.exists(path_2):
        diff = Difference(path_1, path_2)
        print(diff.get_list_columns())

