import pandas as pd


class Difference:
    def __init__(self, path_ts: str, path_fact: str):
        self.data_frame_ts: pd.DataFrame = pd.DataFrame()
        self.data_frame_fact: pd.DataFrame = pd.DataFrame()
        self.path_ts: str = path_ts
        self.path_fact: str = path_fact

    @classmethod
    def is_number_array(cls, array: pd.DataFrame):
        _array = map(lambda val: isinstance(val, float), array.tolist())
        if all(_array):
            return True
        return False

    def get_list_columns(self) -> list | str:
        try:
            self.data_frame_ts: pd.DataFrame = pd.read_excel(self.path_ts)
        except (AttributeError, KeyError):
            return 'TradeError'
        try:
            self.data_frame_fact: pd.DataFrame = pd.read_excel(self.path_fact)
        except (AttributeError, KeyError):
            return 'FactFileError'
        else:
            return self.data_frame_ts.columns.tolist()

    def find_difference_numeric(self, name_column: str) -> list | bool:
        try:
            _select_ts_col: pd.Series = self.data_frame_ts[name_column].dropna(how='all')
            _select_fact_col: pd.Series = self.data_frame_fact[name_column].dropna(how='all')
            if self.is_number_array(_select_ts_col) and self.is_number_array(_select_fact_col):
                _result_difference_num: set = set(_select_ts_col.astype(dtype='int64').tolist()
                                                  ).difference(set(_select_fact_col.astype(dtype='int64').tolist()))
            else:
                _result_difference_num: set = set(_select_ts_col.tolist()
                                                 ).difference(set(_select_fact_col.tolist()))
        except KeyError as err:
            return False
        else:
            return map(str, _result_difference_num)

    def column_is_correct(self):
        try:
            _correct_ts: list = self.data_frame_ts.columns.tolist()
            _correct_fact: list = self.data_frame_fact.columns.tolist()
            _difference_ts_in_fact: set = set(_correct_ts).difference(_correct_fact)
            return _difference_ts_in_fact
        except ValueError as err:
            return err.with_traceback()

