import robin_stocks.robinhood as r
from webull import webull
from datetime import datetime, timedelta
import pandas as pd
import json, time


def rh_login():
    """
    Robinhood Login:
    username: "Your Username" - Most likely your email
    password: "Your Robinhood password to login"

    """
    login = r.authentication.login(username='matthias91.mt@gmail.com', password='Mjt42391!!', expiresIn=None, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')
    if login.get('access_token'):
        print("Good to go! Logged into Robinhood")
        pass


def filter_recent_options(data, expiration=None):
    current_date = datetime.utcnow().date()
    filtered_data = []

    if expiration:
        # If an expiration date is provided, convert it to datetime.date
        expiration_date = datetime.strptime(expiration, "%Y-%m-%d").date()
    else:
        # Use today's date to filter options
        expiration_date = current_date

    for option in data:
        option_expiration = datetime.strptime(option["expiration_date"], "%Y-%m-%d").date()

        if option_expiration == expiration_date:
            # Option with only the specified fields
            filtered_option = {k: v for k, v in option.items() if k in [
                "chain_symbol", "expiration_date", "strike_price", "type",
                "ask_price", "bid_price", "high_price", "low_price",
                "mark_price", "open_interest", "previous_close_price",
                "volume", "delta", "implied_volatility", "theta"
            ]}
            filtered_data.append(filtered_option)

    return filtered_data


def get_quotes(inputSymbols):
    quotes = r.stocks.get_quotes(inputSymbols, info=None)
    extracted_data = [
        {
            "ask_price": item["ask_price"],
            "ask_size": item["ask_size"],
            "bid_price": item["bid_price"],
            "bid_size": item["bid_size"],
            "last_trade_price": item["last_trade_price"],
            "last_extended_hours_trade_price": item["last_extended_hours_trade_price"],
            "previous_close": item["previous_close"],
            "adjusted_previous_close": item["adjusted_previous_close"],
            "trading_halted": item["trading_halted"],
            "state": item["state"]
        }
        for item in quotes
    ]
    formatted_data = json.dumps(extracted_data, indent=4)

    return formatted_data


def buy_options_limit(positionEffect,credOrdeb,price,symbol,quantity,expirationDate,strike,ot,an):
    purchase = r.orders.order_buy_option_limit(positionEffect, credOrdeb, price, symbol, quantity, expirationDate, strike, optionType=ot, account_number=an, timeInForce='gtc', jsonify=True)
    print(purchase)

def sell_options_limit(positionEffect,cOrD,price,symbol,quantity,expirationDate,strike,ot,an):
    purchase = r.orders.order_sell_option_limit(positionEffect, cOrD, price, symbol, quantity, expirationDate, strike, optionType=ot, account_number=an, timeInForce='gtc', jsonify=True)
    print(purchase)

def stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike,ac,type):
    stop_limit = r.orders.order_sell_option_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike, optionType=type, account_number=ac, timeInForce='gtc', jsonify=True)
    print(stop_limit)

def find_options(position=None, cOrd=None,
                 symbol=None, qtity=None, 
                 price=None, type=None, ac=None, 
                 info=None
                 ):
    rh_login()

    print(price)

    find_trades = r.options.find_options_by_strike(
        symbol, strikePrice=str(price), optionType=type, info=info
    )

    # Filter options for the next 5 days from the most recent date
    filtered_options = filter_recent_options(find_trades)

    # Print the formatted JSON data
    formatted_filtered_options = json.dumps(filtered_options, indent=4)
    filtered_options_load = json.loads(formatted_filtered_options)

    print(f"\n{filtered_options_load}")
    if position == 'open':
        symbol = filtered_options_load[0]['chain_symbol']
        date = filtered_options_load[0]['expiration_date']
        strike = filtered_options_load[0]['strike_price']
        type = filtered_options_load[0]['type']
        ask = filtered_options_load[0]['ask_price']
        highs = filtered_options_load[0]['high_price']
        lows = filtered_options_load[0]['low_price']
        mark = filtered_options_load[0]['mark_price']
        open_in = filtered_options_load[0]['open_interest']
        prev_close = filtered_options_load[0]['previous_close_price']
        vol = filtered_options_load[0]['volume']
        delta = filtered_options_load[0]['delta']
        im_vol = filtered_options_load[0]['implied_volatility']
        theta = filtered_options_load[0]['theta']
        buy_options_limit(positionEffect=position,credOrdeb=cOrd,price=ask,
                          symbol=symbol,quantity=qtity,expirationDate=date,
                          strike=strike,ot=type,an=ac)
        time.sleep(30)
        stop_limit(positionEffect='close',creditOrDebit='credit',limitPrice=.02,
                   stopPrice=0.01,symbol=symbol,quantity=1,
                   expirationDate=date,strike=strike,ac=ac,type=type)
    else:
        symbol = filtered_options_load[0]['chain_symbol']
        date = filtered_options_load[0]['expiration_date']
        strike = filtered_options_load[0]['strike_price']
        type = filtered_options_load[0]['type']
        bid = filtered_options_load[0]['bid_price']
        highs = filtered_options_load[0]['high_price']
        lows = filtered_options_load[0]['low_price']
        mark = filtered_options_load[0]['mark_price']
        open_in = filtered_options_load[0]['open_interest']
        prev_close = filtered_options_load[0]['previous_close_price']
        vol = filtered_options_load[0]['volume']
        delta = filtered_options_load[0]['delta']
        im_vol = filtered_options_load[0]['implied_volatility']
        theta = filtered_options_load[0]['theta']


#if __name__ == '__main__':
#    find_options(position='open', cOrd='debit', symbol='SPY', 
#                 qtity=1, strike=540.00, 
#                 type='put', ac='120853833')
