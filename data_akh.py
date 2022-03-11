import akshare as ak
import pandas as pd


class AkData:
    def __init__(self, sheet, start, end):
        self.future_product = sheet
        self.start_date = start
        self.end_date = end

    def get_data(self):
        index = ['Day', 'Open', 'High', 'Low', 'Close', 'Vol', 'CCL', 'Dyn']
        for i in self.future_product:
            df = ak.futures_main_sina(symbol=i, start_date=self.start_date, end_date=self.end_date)
            df.columns = index
            df.to_csv(f"./Data_csv/{i}.csv")


class DataProcess:
    def __init__(self, sheet):
        self.lst = []
        self.sheet = sheet
        self.range = 100000

        self.__get_data()

    def __get_range(self):
        for i in self.sheet:
            df = pd.read_csv(f"./Data_csv/{i}.csv")
            self.range = min(self.range, len(df.index))

    def __get_data(self):
        self.__get_range()
        for i in self.sheet:
            df = pd.read_csv(f"./Data_csv/{i}.csv")
            del df['Unnamed: 0']
            df = df.iloc[len(df.index) - self.range:]
            df = df.reset_index(drop=True)
            self.lst.append(df)



