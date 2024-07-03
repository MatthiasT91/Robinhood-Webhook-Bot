from robinhood.authentication import login
from robinhood.stocks import get_quotes
from robinhood.orders import order_buy_option_limit, order_sell_option_limit, order_sell_option_stop_limit
from robinhood.options import find_options_by_strike
from datetime import datetime
import datetime
from discord import SyncWebhook
import json
import pytz
import math
import requests
from scipy.stats import norm


def discord_message(messages,settings):
    webhook_url = settings.get('webhook')
    if webhook_url == None:
        return
    webhook = SyncWebhook.from_url(url=webhook_url)
    webhook.send(content=f"```{messages}```")


def read_order_results_from_file(filename='orders.txt'):
    try:
        with open(filename, 'r') as file:
            orders = json.load(file)
        return orders
    except Exception as e:
        print(f"Error reading orders from {filename}: {e}")
        return None


def debug_messages(app,messages):
    if app == None:
        print(f"{messages}")
        return
    else:
        app.logger.info(f"{messages}")
        return


def rh_login(app,settings):
    """
    Robinhood Login:
    username: "Your Username" - Most likely your email
    password: "Your Robinhood password to login"

    """
    logins = login(username=settings.get('username'), password=settings.get('password'), expiresIn=None, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')

    if logins.get('access_token'):
        debug_messages(app,"Good to go! Logged into Robinhood")
        pass


def filter_recent_options(data, expiration=None):
    # Get the current date and time in UTC
    current_datetime_utc = datetime.datetime.utcnow()
    
    # Convert UTC to Eastern Time
    eastern = pytz.timezone('US/Eastern')
    current_datetime_est = current_datetime_utc.astimezone(eastern)
    
    # Get current date in EST
    current_date = current_datetime_est.date()
    current_time = current_datetime_est.time()
    
    filtered_data = []

    if expiration:
        # If an expiration date is provided, convert it to datetime.date
        expiration_date = datetime.datetime.strptime(expiration, "%Y-%m-%d").date()
    else:
        # If no expiration date is provided, find the nearest expiration date
        future_expirations = sorted(set(
            datetime.datetime.strptime(option["expiration_date"], "%Y-%m-%d").date() for option in data
            if datetime.datetime.strptime(option["expiration_date"], "%Y-%m-%d").date() >= current_date
        ))
        if future_expirations:
            expiration_date = future_expirations[0]
        else:
            # If no future expiration dates found, set a default far future date to avoid filtering all options out
            expiration_date = current_date + datetime.timedelta(days=365)

    for option in data:
        option_expiration = datetime.datetime.strptime(option["expiration_date"], "%Y-%m-%d").date()

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
    quotes = get_quotes(inputSymbols, info=None)
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
    purchase = order_buy_option_limit(positionEffect, credOrdeb, price, symbol, quantity, expirationDate, strike, optionType=ot, account_number=an, timeInForce='gtc', jsonify=True)
    print(purchase)
    return purchase


def sell_options_limit(positionEffect,cOrD,price,symbol,quantity,expirationDate,strike,ot,an):
    purchase = order_sell_option_limit(positionEffect, cOrD, price, symbol, quantity, expirationDate, strike, optionType=ot, account_number=an, timeInForce='gtc', jsonify=True)
    print(purchase)
    return purchase


# Not being used ->
def get_treasury_yield(series_id):
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key=288ca63ff70507816a2a421702db28f0&file_type=json'
    response = requests.get(url)
    data = response.json()

    if 'observations' not in data or not data.get('observations'):
        raise ValueError('No data found for the given series ID.')
    
    # Get the most recent yield
    latest_data = data.get('observations')[-1]  # Assuming the most recent data is the last entry
    risk_free_rate = float(latest_data.get('value')) / 100  # Convert percentage to decimal
    return risk_free_rate


def get_risk_free_rate(expiration_date_str):
    expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
    today = datetime.date.today()
    days_to_expiration = (expiration_date - today).days

    if days_to_expiration <= 31:
        series_id = 'DGS1MO'  # 1-month Treasury yield
    elif days_to_expiration <= 92:
        series_id = 'DGS3MO'  # 3-month Treasury yield
    else:
        series_id = 'DGS6MO'  # 6-month Treasury yield (or you can choose another)
    return get_treasury_yield(series_id=series_id)


def black_scholes(S, K, T, r, sigma, option_type):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    print(S)
    print(K)
    print(T)
    print(r)
    print(sigma)

    # Debug prints to trace the computation
    print(f"S: {S}, K: {K}, T: {T}, r: {r}, sigma: {sigma}")

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    print(f"d1: {d1}, d2: {d2}")

    if option_type == 'call':
        option_price = (S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2))
    elif option_type == 'put':
        option_price = (K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    print(f"Option Price: {option_price}")

    return option_price
# <-


def calculate_option_prices(options_data, options_type, stock_price, risk_free_rate):
    current_date = datetime.datetime.utcnow().date()
    eastern = pytz.timezone('US/Eastern')
    current_datetime_est = datetime.datetime.now(eastern)

    calculated_prices = []

    for option in options_data:
        strike_price = float(option.get('legs')[0]['strike_price'])
        expiration_date = datetime.datetime.strptime(option.get('legs')[0]['expiration_date'], '%Y-%m-%d').date()
        days_to_expiration = (expiration_date - current_date).days
        time_to_expiration = days_to_expiration / 365.0
        implied_volatility = float(option.get('implied_volatility')) / 100.0  # Convert percentage to decimal
        option_price = black_scholes(strike_price, stock_price, time_to_expiration, risk_free_rate, implied_volatility, options_type)
        option['calculated_price'] = option_price

        calculated_prices.append(option)

    return calculated_prices


def options_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike,ac,type):
    stop_limit = order_sell_option_stop_limit(positionEffect, creditOrDebit, limitPrice,
                                              stopPrice, symbol, quantity, expirationDate,
                                              strike, optionType=type, account_number=ac,
                                              timeInForce='gtc', jsonify=True)
    print(stop_limit)
    return stop_limit


def round_up(price):
    return (price * 2 + 1) // 1 / 2


def round_down(price):
    return (price * 2 - 1) // 1 / 2


def round_to_nearest_half(price):
    # Round the price to the nearest 0.50
    rounded_price = round(float(price) * 2) / 2
    return rounded_price


def find_options(position, cOrd,symbol, qtity, 
                 price1, price2, strike, expiration, 
                 option_type, type, info, app, settings):
    
    rh_login(app,settings)

    if price1:
        rounded_price = round_to_nearest_half(price1)
        find_trades = find_options_by_strike(
            symbol, strikePrice=str(rounded_price), optionType=type, info=info
        )
        while not find_trades:
            if option_type.lower() == "call":  # ITM
                rounded_price = round_down(float(rounded_price))
            elif option_type.lower() == "put":  # ITM
                rounded_price = round_up(float(rounded_price))

            find_trades = find_options_by_strike(
                symbol, strikePrice=str(rounded_price), optionType=option_type, info=info
            )

            # If rounding down or up results in the same price, break to avoid an infinite loop
            if rounded_price == round_to_nearest_half(rounded_price):
                # Filter options for the next 5 days from the most recent date
                break

        filtered_options = filter_recent_options(find_trades)
    if strike:
        find_trades = find_options_by_strike(
            symbol, strikePrice=str(strike), optionType=type, info=info
        )

        # Filter options for the next 5 days from the most recent date
        filtered_options = filter_recent_options(find_trades)

    # Print the formatted JSON data
    formatted_filtered_options = json.dumps(filtered_options, indent=4)

    filtered_options_load = json.loads(formatted_filtered_options)

    if position == 'open':
        if type == 'call':
            symbol = filtered_options_load[0]['chain_symbol']
            date   = filtered_options_load[0]['expiration_date']
            strike = filtered_options_load[0]['strike_price']
            type   = filtered_options_load[0]['type']
            ask    = filtered_options_load[0]['ask_price']

            orders = buy_options_limit(positionEffect=position,credOrdeb=cOrd,price=ask,
                              symbol=symbol,quantity=qtity,expirationDate=date,
                              strike=strike,ot=type,an=settings.get('accountid'))

        else:
            symbol = filtered_options_load[0]['chain_symbol']
            date   = filtered_options_load[0]['expiration_date']
            strike = filtered_options_load[0]['strike_price']
            type   = filtered_options_load[0]['type']
            ask    = filtered_options_load[0]['ask_price']

            orders = buy_options_limit(positionEffect=position,credOrdeb=cOrd,price=ask,
                              symbol=symbol,quantity=qtity,expirationDate=date,
                              strike=strike,ot=type,an=settings.get('accountid'))

    else:
        symbol_close = filtered_options_load[0]['chain_symbol']
        date_close = filtered_options_load[0]['expiration_date']
        strike_close = filtered_options_load[0]['strike_price']
        type_close = filtered_options_load[0]['type']
        bid_close    = filtered_options_load[0]['bid_price']

<<<<<<< HEAD
        orders = sell_options_limit(positionEffect=position,cOrD=cOrd,price=bid_close,
                              symbol=symbol_close,quantity=qtity,expirationDate=date_close,
                              strike=strike_close,ot=type_close,an=settings.get('accountid'))
    
    if orders: 
        print("Sending back")
        return
=======

#if __name__ == '__main__':
#    find_options(position='open', cOrd='debit', symbol='SPY', 
#                 qtity=1, strike=540.00, 
#                 type='put', ac='')
>>>>>>> e082c8c7b9088abffe69823655f07be220b52239
