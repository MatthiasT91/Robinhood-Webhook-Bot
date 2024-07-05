from robinhood.authentication import login
from robinhood.stocks import get_quotes
from robinhood.orders import order_buy_option_limit, order_sell_option_limit, order_sell_option_stop_limit
from robinhood.options import find_options_by_strike
from datetime import datetime,time,timedelta
from discord import SyncWebhook
import json
import pytz
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
    current_datetime_utc = datetime.utcnow()
    
    # Convert UTC to Eastern Time
    eastern = pytz.timezone('US/Eastern')
    current_datetime_est = current_datetime_utc.astimezone(eastern)
    
    # Get current date in EST
    current_date = current_datetime_est.date()
    current_time = current_datetime_est.time()
    
    filtered_data = []

    if expiration:
        # If an expiration date is provided, convert it to datetime.date
        expiration_date = datetime.strptime(expiration, "%Y-%m-%d").date()
    else:
        # If no expiration date is provided, find the nearest expiration date
        future_expirations = sorted(set(
            datetime.strptime(option["expiration_date"], "%Y-%m-%d").date() for option in data
            if datetime.strptime(option["expiration_date"], "%Y-%m-%d").date() >= current_date
        ))
        if future_expirations:
            expiration_date = future_expirations[0]
        else:
            # If no future expiration dates found, set a default far future date to avoid filtering all options out
            expiration_date = current_date + timedelta(days=365)

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
    return purchase


def sell_options_limit(positionEffect,cOrD,price,symbol,quantity,expirationDate,strike,ot,an):
    purchase = order_sell_option_limit(positionEffect, cOrD, price, symbol, quantity, expirationDate, strike, optionType=ot, account_number=an, timeInForce='gtc', jsonify=True)
    return purchase


def options_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike,ac,type):
    stop_limit = order_sell_option_stop_limit(positionEffect, creditOrDebit, limitPrice,
                                              stopPrice, symbol, quantity, expirationDate,
                                              strike, optionType=type, account_number=ac,
                                              timeInForce='gtc', jsonify=True)
    return stop_limit


def round_up(price):
    return (price * 2 + 1) // 1 / 2


def round_down(price):
    return (price * 2 - 1) // 1 / 2


def round_to_nearest_half(price):
    # Round the price to the nearest 0.50
    rounded_price = round(float(price) * 2) / 2
    return rounded_price


def is_market_open():
    # Define the EST timezone
    est = pytz.timezone('US/Eastern')

    # Get the current time in EST
    now = datetime.now(est)
    current_time = now.time()
    current_day = now.date()
    weekday = now.weekday()  # Monday is 0 and Sunday is 6

    # Define the market hours
    market_open = time(9, 30)   # 9:30 AM
    market_close = time(16, 0)  # 4:00 PM

    # List of market holidays (add more as needed)
    holidays = [
        '2024-01-01',  # New Year's Day
        '2024-01-15',  # Martin Luther King Jr. Day
        '2024-02-19',  # Presidents' Day
        '2024-03-29',  # Good Friday
        '2024-05-27',  # Memorial Day
        '2024-06-19',  # Juneteenth National Independence Day
        '2024-07-04',  # Independence Day
        '2024-09-02',  # Labor Day
        '2024-11-28',  # Thanksgiving Day
        '2024-12-25',  # Christmas Day
    ]

    # Check if today is a holiday
    today_str = current_day.strftime('%Y-%m-%d')
    if today_str in holidays:
        return False

    # Check if today is a weekday (Monday to Friday)
    if weekday < 0 or weekday > 4:
        return False

    # Check if the current time is within market hours
    if market_open <= current_time < market_close:
        return True
    else:
        return False


def format_order_message(order,stock_position,option):
    symbol = order.get('symbol')
    fees = order.get('fees')
    price = order.get('price')
    quantity = order.get('quantity')
    side = order.get('side')
    state = order.get('updstateated_at')

    message = (
        f"\nOrder Data for {option}:\n"
        f"----------------------\n"
        f"Symbol: {symbol}\n"
        f"Price: {price}\n"
        f"Quantity: {quantity}\n"
        f"Fees: {fees}\n"
        f"Type: {stock_position}\n"
        f"Side: {side}\n"
        f"State: {state}\n"
        f"----------------------\n",
    )

    return message


def find_options(position, cOrd,symbol, qtity, 
                 price1, price2, strike, expiration, 
                 option_type, type, app, settings):
    
    rh_login(app,settings)
    if is_market_open():
        if price1:
            rounded_price = round_to_nearest_half(price1)
            find_trades = find_options_by_strike(
                symbol, strikePrice=str(rounded_price), optionType=type, info=None
            )
            while not find_trades:
                if option_type.lower() == "call":  # ITM
                    rounded_price = round_down(float(rounded_price))
                elif option_type.lower() == "put":  # ITM
                    rounded_price = round_up(float(rounded_price))

                find_trades = find_options_by_strike(
                    symbol, strikePrice=str(rounded_price), optionType=option_type, info=None
                )

                # If rounding down or up results in the same price, break to avoid an infinite loop
                if rounded_price == round_to_nearest_half(rounded_price):
                    # Filter options for the next 5 days from the most recent date
                    break

            filtered_options = filter_recent_options(find_trades)
        if strike:
            find_trades = find_options_by_strike(
                symbol, strikePrice=str(strike), optionType=type, info=None
            )

            # Filter options for the next 5 days from the most recent date
            filtered_options = filter_recent_options(find_trades)
    else:
        return

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

        orders = sell_options_limit(positionEffect=position,cOrD=cOrd,price=bid_close,
                              symbol=symbol_close,quantity=qtity,expirationDate=date_close,
                              strike=strike_close,ot=type_close,an=settings.get('accountid'))
    
    if orders: 
        order_info = format_order_message(orders,position,'Options')
        discord_message(order_info,settings)
        
        return
