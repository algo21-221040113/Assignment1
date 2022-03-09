import pandas as pd
class BackTest:
    def __init__(self, sheet, data, r, h, time_length):
        self.sheet = sheet  ##future product
        self.R = r  ##signal time
        self.H = h  ##on pos time
        self.data = data  ##original data
        self.time_length = time_length  # backtest_time_length
        self.posit = 100000
        self.real_pos = False
        self.net = False

        self.__strategy_init()

    def __strategy_init(self):
        for i in range(len(self.data)):
            self.data[i]['Momentum'] = self.data[i]['Close'].pct_change(periods=self.R)

    def run_backtest(self):
        self.net = [0] * (self.R - 1)
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
                if pos == 0:
                    pos = 1
                    self.real_pos = pd.DataFrame(index_pos, columns=['index'])
                self.real_pos['index'] = index_pos
                self.real_pos['directione'] = dir_pos
                self.real_pos['pos'] = pos_pos
                self.real_pos['net'] = net_pos
                self.net.append(self.real_pos['net'].sum())






