import pandas as pd
import numpy as np


class BackTest:
    def __init__(self, sheet, data, r, h, time_length):
        self.sheet = sheet  ##future product
        self.R = r  ##signal time
        self.H = h  ##on pos time
        self.data = data  ##original data
        self.time_length = time_length  # backtest_time_length
        self.posit = 1000000
        self.real_pos = False
        self.net = False
        self.net_lst = False
        self.profit = False
        self.profit_lst = []

        self.annual = False
        self.sharp = False

        self.__strategy_init()

    def __strategy_init(self):
        for i in range(len(self.data)):
            self.data[i]['Momentum'] = self.data[i]['Close'].pct_change(periods=self.R)

    def run_backtest(self):
        self.net_lst = [0] * (self.R)
        self.profit = 0
        pos = 0
        for i in range(self.R, self.time_length):
            if (i - self.R) % self.H == 0:
                ##signal
                signal = []
                close = []
                direct = [1] * 3 + [0] * 25 + [-1] * 3
                for j in self.data:
                    signal.append(j.iloc[i]['Momentum'])
                    close.append(j.iloc[i]['Close'])
                sig_df = pd.DataFrame(self.sheet, columns=['future'])
                sig_df['signal'] = signal
                sig_df['close'] = close
                sig_df.sort_values(by='signal', ascending=False, inplace=True)
                sig_df['dire'] = direct
                sig_df['pos'] = self.posit // sig_df['close']

                if pos == 0:
                    dir_pos = []
                    index_pos = []
                    pos_pos = []
                    net_pos = []
                    for k in range(len(self.data)):
                        if sig_df.loc[k]['dire'] != 0:
                            index_pos.append(k)
                            dir_pos.append(sig_df.loc[k]['dire'])
                            pos_pos.append(sig_df.loc[k]['pos'])
                            net_pos.append(sig_df.loc[k]['pos'] * sig_df.loc[k]['close'])

                    self.real_pos = pd.DataFrame(index_pos, columns=['index'])
                    self.real_pos['index'] = index_pos
                    self.real_pos['direction'] = dir_pos
                    self.real_pos['pos'] = pos_pos
                    self.real_pos['net'] = net_pos
                    self.net = self.real_pos['net'].sum()
                    self.net_lst.append(self.net)

                    pos = 1
                else:
                    # sell
                    self.profit = 0
                    for j in range(6):
                        index = int(self.real_pos.loc[j]['index'])
                        direction = self.real_pos.loc[j]['direction']
                        pos = self.real_pos.loc[j]['pos']
                        self.profit += (self.data[index].iloc[i]['Close'] - self.data[index].iloc[i - 1][
                            'Close']) * pos * direction

                    self.net += self.profit
                    self.profit_lst.append(self.profit)

                    self.net_lst.append(self.net)

                    # buy
                    dir_pos = []
                    index_pos = []
                    pos_pos = []
                    net_pos = []
                    for k in range(len(self.data)):
                        if sig_df.loc[k]['dire'] != 0:
                            index_pos.append(k)
                            dir_pos.append(sig_df.loc[k]['dire'])
                            pos_pos.append(sig_df.loc[k]['pos'])
                            net_pos.append(sig_df.loc[k]['pos'] * sig_df.loc[k]['close'])

                    self.real_pos['index'] = index_pos
                    self.real_pos['index'] = index_pos
                    self.real_pos['direction'] = dir_pos
                    self.real_pos['pos'] = pos_pos
                    self.real_pos['net'] = net_pos



            else:
                self.profit = 0
                for j in range(6):
                    index = int(self.real_pos.loc[j]['index'])
                    direction = self.real_pos.loc[j]['direction']
                    pos = self.real_pos.loc[j]['pos']
                    self.profit += (self.data[index].iloc[i]['Close'] - self.data[index].iloc[i - 1][
                        'Close']) * pos * direction

                self.net += self.profit
                self.profit_lst.append(self.profit)
                self.net_lst.append(self.net)

    def result(self):
        self.net_lst = self.net_lst[self.R:]

        self.annual = sum(self.profit_lst) * 250 / (self.net_lst[0] * self.time_length)
        self.sharp = (self.annual - 0.03) / np.std(self.profit_lst / self.net_lst[0])

    def plot_result(self):

        df = pd.DataFrame(self.net_lst, columns=["net"])
        df = df.set_index(self.data[1].iloc[self.R:]['Day'])
        df.plot.line()










