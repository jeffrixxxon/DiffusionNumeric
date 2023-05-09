import os
import pandas as pd


class Difference:
    def __init__(self, path_ts: str, path_fact: str):
        self.new_frame = pd.DataFrame(dtype='Int64')
        self.data_frame_ts = pd.DataFrame(dtype='Int64')
        self.data_frame_fact = pd.DataFrame(dtype='Int64')
        self.ts: str = path_ts
        self.fact: str = path_fact

    def get_list_columns(self) -> list:
        self.data_frame_ts = pd.read_excel(self.ts)
        self.data_frame_fact = pd.read_excel(self.fact)
        return self.data_frame_ts.columns.tolist()

    def find_difference_numeric(self, name_column: str) -> list:
        _trade = self.data_frame_ts[name_column].tolist()
        _fact = self.data_frame_fact[name_column].tolist()
        _result_difference_num = set(_trade).difference(set(_fact))
        return list(map(str, _result_difference_num))

