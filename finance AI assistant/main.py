from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf

import pickle
import sys
import datetime as dt

portfolio = {'AAPL': 20, 'TSLA': 5, 'GS': 10}

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

def save_portfolio(portfolio):
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)

def add_portfolio():
    ticker = input("Which stock would you like to add? ")
    amount = input("How many shares would you like to add? ")
    if ticker in portfolio:
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)

    save_portfolio()

def remove_portfolio():
    ticker = input("Which stock would you like to sell? ")
    amount = input("How many shares would you like to sell? ")
    if ticker in portfolio.keys():
        if amount <= portfolio[ticker]:
            portfolio[ticker] -= int(amount)
            if portfolio[ticker] == 0:
                del portfolio[ticker]
            save_portfolio()
        else:
            print("You don't have that many shares")

    else:
        print("You don't have that stock")

def show_portfolio():
    print("Your portfolio:")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}" )

def portfolio_worth():
    sum = 0
    for ticker in portfolio.keys():
        data = web.DataReader(ticker, 'yahoo')
        price = data['close'].iloc[-1] 
        sum += price
    print(f"Your portfolio is worth ${sum}")

def portfolio_gains():
    starting_date = input("What is the starting date? (YYYY-MM-DD) ")
    sum_now = 0
    sum_then = 0
    try:
        for ticker in portfolio.keys():
            data = web.DataReader(ticker, 'yahoo', start=starting_date)
            price_now = data['close'].iloc[-1]
            price_then = data.loc[data.index == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then

        print(f"Relative Gains: {((sum_now - sum_then) / sum_then) * 100}%")  
        print(f"Absolute Gains: ${sum_now - sum_then}")
    except IndexError:
        print("Invalid date")

def plot_chart():
    ticker = input("Choose a ticker symbol:")
    starting_string = input("What is the starting date? (YYYY-MM-DD) ")
    plt.style.use('dark_background')
    start = dt.datetime.strptime(starting_string, '%Y-%m-%d')
    end = dt.datetime.now()
    data = web.DataReader(ticker, 'yahoo', start=start, end=end)
    colors = mpf.make_marketcolors(up='g', down='r', edge='i', wick='i', volume='in', ohlc='i')
    mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=colors, gridstyle='-', y_on_right=False)
    mpf.plot(data, type='candle', style=mpf_style, volume=True, title=ticker)

def bye():
    print("Goodbye!")
    sys.exit(0) 


mappings = {
    'plot_chart': plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
    'bye': bye
}

assistant = GenericAssistant('intents.json', mappings, "finance_assistant")
assistant.train_model()
assistant.save_model()

while True:
    message = input("What would you like to do? ")
    assistant.request(message)



    
