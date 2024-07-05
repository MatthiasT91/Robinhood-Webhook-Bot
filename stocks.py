from robinhood.authentication import login
from robinhood.orders import order_sell_market, order_buy_limit, \
    order_sell_limit, order_buy_market, order_buy_fractional_by_quantity, \
    order_sell_fractional_by_quantity
from discord import SyncWebhook



def debug_messages(app,messages):
    if app == None:
        print(f"{messages}")
        return
    else:
        app.logger.info(f"{messages}")
        return


def discord_message(messages,settings):
    webhook_url = settings.get('webhook')
    if webhook_url == None:
        return
    webhook = SyncWebhook.from_url(url=webhook_url)
    webhook.send(content=f"```{messages}```")


def rh_login(app,settings):
    """
    Robinhood Login:
    username: "Your Username" - Most likely your email
    password: "Your Robinhood password to login"

    """
    user = settings.get('username')
    password = settings.get('password')
    logins = login(username=user, password=password, expiresIn=None, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')
    if logins.get('access_token'):
        debug_messages(app,"Good to go! Logged into Robinhood")
        pass


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


def find_stocks(position, symbol, qtity, price1, type, app, settings):
    rh_login(app,settings)

    if position == 'market':
        if type == 'buy':
            if qtity < '1.0':
                order = order_buy_fractional_by_quantity(symbol, float(qtity), account_number=settings.get('accountid'), timeInForce='gfd', extendedHours=False, jsonify=True)
            else:
                order = order_buy_market(symbol, float(qtity), account_number=settings.get('accountid'),timeInForce='gtc', extendedHours=False, jsonify=True)
        else:
            if qtity < '1.0':
                order = order_sell_fractional_by_quantity(symbol, float(qtity), account_number=settings.get('accountid'), timeInForce='gfd', priceType='bid_price',extendedHours=False, jsonify=True,market_hours='extendedHours')
            else:
                order = order_sell_market(symbol, float(qtity), account_number=settings.get('accountid'),timeInForce='gtc', extendedHours=False, jsonify=True)
    else:
        if type == 'buy':
            if qtity < '1.0':
                order = order_buy_fractional_by_quantity(symbol, float(qtity), account_number=settings.get('accountid'), timeInForce='gfd', extendedHours=False, jsonify=True)
            else:
                order = order_buy_limit(symbol, float(qtity), price1, account_number=settings.get('accountid'),timeInForce='gtc', extendedHours=False, jsonify=True)
        else:
            if qtity < '1.0':
                order = order_sell_fractional_by_quantity(symbol, float(qtity), account_number=settings.get('accountid'), timeInForce='gfd', priceType='bid_price',extendedHours=False, jsonify=True,market_hours='extendedHours')
            else:
                order = order_sell_limit(symbol, float(qtity), price1, account_number=settings.get('accountid'),timeInForce='gtc', extendedHours=False, jsonify=True)
    
    if order: 
        order_info = format_order_message(order,position,'Stocks')
        discord_message(order_info,settings)
        
        return
