from data_akh import AkData,DataProcess
from BackTest import BackTest
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


##test from diffrent R and H

time_table = [10,20,60,120,250]
annual_pd = pd.DataFrame(index=('10','20','60','120','250'))
sharp_pd = pd.DataFrame(index=('10','20','60','120','250'))

if __name__ == "__main__":
    sheet = ["V0","P0","M0","I0","L0","C0","Y0","A0","J0","JM0","CS0","TA0","OI0","RM0","ZC0","SR0","CF0",
             "MA0","FG0","SF0","SM0","FU0","AL0","RU0","ZN0","CU0","AU0","RB0","BU0","NI0","SN0"]

    start_date = "20000101"
    end_date = "20220101"

    ## get data from akshare
    '''get_data = AkData(sheet,start_date,end_date)'''
    '''get_data.get_data()'''

    ##process data
    data = DataProcess(sheet)

    ##backtest example
    ex = BackTest(sheet, data.lst, 10, 20, data.range)
    ex.run_backtest()
    ex.result()
    ex.plot_result()
    print(f"the annual rate is {ex.annual}")
    print(f"the sharp ratio is {ex.sharp}")


    ##experiment
    for i in time_table:
        annual_lst = []
        sharp_lst = []
        for j in time_table:
            a = BackTest(sheet, data.lst, j, i, data.range)
            a.run_backtest()
            a.result()
            annual_lst.append(a.annual)
            sharp_lst.append(a.sharp)
        annual_pd[str(i)] = annual_lst
        sharp_pd[str(i)] = sharp_lst


    ##plot
    fig, ax = plt.subplots(figsize=(9, 9))
    sns.heatmap(annual_pd, annot=True, vmax=max(annual_pd.max()), vmin=min(annual_pd.min()), xticklabels=True,
                yticklabels=True, square=True, cmap="YlGnBu")

    ax.set_title('Annual_rate', fontsize=18)
    ax.set_ylabel('R', fontsize=18)
    ax.set_xlabel('H', fontsize=18)


    plt.show()






