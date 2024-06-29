import robin_stocks.robinhood as r
from datetime import datetime, timedelta
from discord import SyncWebhook
import pandas as pd
import json, time
import pytz
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def discord_message(messages):
    webhook_url = config['ACCOUNTINFO']['webhook']
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
    user = config['ACCOUNTINFO']['username']
    passw = config['ACCOUNTINFO']['password']
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

def crypto_robinhood(symbol,quantity,limitPrice,app):
    rh_login(app)
    crypto_limit_order(symbol,quantity,limitPrice)