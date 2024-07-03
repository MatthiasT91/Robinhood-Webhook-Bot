from robinhood.authentication import login
from robinhood.orders import order_sell_market, order_buy_limit, \
    order_sell_limit, order_buy_market
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


def stock_limit_buy_order(symbol, quantity, limitPrice, exHours, ac):
    orders = order_buy_limit(symbol, quantity, limitPrice, account_number=ac,
                                    timeInForce='gtc', extendedHours=exHours, jsonify=True)
    return orders


def stock_limit_sell_order(symbol, quantity, limitPrice, exHours, ac):
    orders = order_sell_limit(symbol, quantity, limitPrice, account_number=ac,
                                    timeInForce='gtc', extendedHours=exHours, jsonify=True)
    return orders


def stock_market_sell_order(symbol, quantity, exHours, ac):
    orders = order_sell_market(symbol, quantity, account_number=ac,
                                    timeInForce='gtc', extendedHours=exHours, jsonify=True)
    return orders


def stock_market_buy_order(symbol, quantity, exHours, ac):
    orders = order_buy_market(symbol, quantity, account_number=ac,
                                    timeInForce='gtc', extendedHours=exHours, jsonify=True)
    return orders


def find_stocks(position=None, symbol=None, qtity=None, price1=None, 
                 type=None, app=None, settings=None):
    
    rh_login(app,settings)

    if position == 'market':
        if type == 'buy':
            order = stock_market_buy_order(symbol,qtity,False,settings.get('accountid'))
        else:
            order = stock_market_sell_order(symbol,qtity,False,settings.get('accountid'))
    else:
        if type == 'buy':
            order = stock_limit_buy_order(symbol,qtity,price1,False,settings.get('accountid'))
        else:
            order = stock_limit_sell_order(symbol,qtity,price1,False,settings.get('accountid'))
    
    if order: 
        print("Sending back")
        return
