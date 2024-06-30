from robinhood.authentication import login
from robinhood.crypto import get_crypto_currency_pairs
from robinhood.orders import order_buy_crypto_by_quantity,order_sell_crypto_by_quantity,\
    order_buy_crypto_limit,order_sell_crypto_limit
from discord import SyncWebhook
import pandas as pd
import json, time
import pytz
import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

def discord_message(messages):
    webhook_url = os.getenv('webhook')
    if webhook_url == None:
        return
    webhook = SyncWebhook.from_url(url=webhook_url)
    webhook.send(content=f"```{messages}```")


def rh_login(app):
    """
    Robinhood Login:
    username: "Your Username" - Most likely your email
    password: "Your Robinhood password to login"

    """
    user = os.getenv('username')
    passw = os.getenv('password')
    app.logger.info(f'Username: {user}')
    app.logger.info(f'Password: {passw}')
    login = r.authentication.login(username=user, password=passw, expiresIn=None, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')
    if login.get('access_token'):
        print("Good to go! Logged into Robinhood")
        pass

def crypto_limit_order(symbol,quantity,limitPrice):
    orders = r.orders.order_buy_crypto_limit(symbol, quantity, limitPrice, timeInForce='gtc', jsonify=True)
    discord_message(orders)
    print(orders)

def crypto_robinhood(symbol, quantity, price, stock_type, stock_position, app):
    rh_login(app)
    creating_order = crypto_order(symbol, quantity, price, stock_type, stock_position, app)
    if creating_order:
        order_details = extract_order_details(creating_order)
        order_info = format_order_message(order_details)
        discord_message(order_info)
        debug_messages(app,order_info)

#if __name__ == '__main__':
#    crypto_robinhood('DOGEUSDT',5,0.12196,'buy',None)