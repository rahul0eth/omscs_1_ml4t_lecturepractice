import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="data"):
    #returns CSV file path for given symbol
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    #gets Adj close for given symbols and dates
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol),index_col="Date",parse_dates=True,usecols=["Date","Adj Close"],na_values=['nan'])

        #rename column to prevent clash
        df_temp = df_temp.rename(columns={'Adj Close': symbol})

        df = df.join(df_temp)
        if symbol == 'SPY':
            df = df.dropna(subset=["SPY"])

    return df

def normalize_data(df):
    return df/df.ix[0,:]

def plot_data(df,title="Stock Prices"):
    ax = df.plot(title=title,fontsize=8)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ")
    plt.show()

def plot_selected(df,columns,sd,ed):
    df_sliced = df.ix[sd:ed,columns]
    plot_data(df_sliced)

def test_run():
    dates = pd.date_range('2010-01-01', '2010-12-31 ')
    symbols = ['GOOG', 'IBM', 'GLD']

    df = get_data(symbols,dates)

    sd='2010-03-01'
    ed='2010-04-01'
    sym = ['SPY','IBM']

    #print(df.ix[sd:ed,sym])
    plot_data(normalize_data(df))
    #plot_selected(df,sym,sd,ed)

if __name__ == "__main__":
    test_run()
