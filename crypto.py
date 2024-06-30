from robinhood.authentication import login
from robinhood.crypto import get_crypto_currency_pairs
from robinhood.orders import order_buy_crypto_by_quantity,order_sell_crypto_by_quantity,\
    order_buy_crypto_limit,order_sell_crypto_limit
from discord import SyncWebhook



def rh_login(app):
    """
    Robinhood Login:
    username: "Your Username" - Most likely your email
    password: "Your Robinhood password to login"

    """
    logins = login(username='matthias91.mt@gmail.com', password='Mjt42391!!', expiresIn=None, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')

    if logins.get('access_token'):
        debug_messages(app,"Good to go! Logged into Robinhood")
        pass


def discord_message(messages):
    webhook = SyncWebhook.from_url(url='https://discord.com/api/webhooks/1226801531337048096/sKmFCuqJ5CzSWBIaTsA-d9pP_tZzzwWtoxncBMuR-CQjM-d4BcPH12T27XLDATN6Nmvd')
    webhook.send(content=f"```{messages}```")
    return


def debug_messages(app,messages):
    if app == None:
        print(f"{messages}")
        return
    else:
        app.logger.info(f"{messages}")
        return


def format_order_message(order):
    symbol = order.get('symbol')
    created_at = order.get('created_at')
    price = order.get('price')
    quantity = order.get('quantity')
    side = order.get('side')
    updated_at = order.get('updated_at')

    message = (
        f"*Order Details*\n"
        f"Symbol: {symbol}\n"
        f"Created At: {created_at}\n"
        f"Price: {round(float(price),4)}\n"
        f"Quantity: {round(float(quantity),4)}\n"
        f"Side: {side}\n"
        f"Updated At: {updated_at}\n"
    )

    return message


def extract_order_details(order_response):
    symbol = order_response.get('currency_code')
    created_at = order_response.get('created_at')
    price = order_response.get('price')
    quantity = order_response.get('quantity')
    side = order_response.get('side')
    updated_at = order_response.get('updated_at')
    
    return {
        'symbol': symbol,
        'created_at': created_at,
        'price': price,
        'quantity': quantity,
        'side': side,
        'updated_at': updated_at
    }


def crypto_order(symbol, quantity, price, stock_type, stock_position, app=None):
    # Get the list of crypto currency pairs
    crypto_pairs = get_crypto_currency_pairs(info=None)
    
    # Remove "USDT" or "USDC" from the end of the symbol if they exist
    if symbol.endswith("USDT"):
        stripped_symbol = symbol[:-4] + "-USD"  # Remove the last 4 characters ("USDT")
    elif symbol.endswith("USDC"):
        stripped_symbol = symbol[:-4] + "-USD"  # Remove the last 4 characters ("USDC")
    elif symbol.endswith("USD"):
        stripped_symbol = symbol[:-3] + "-USD"  # Remove the last 4 characters ("USDC")
    else:
        stripped_symbol = symbol

    # Find the specific crypto pair for the given stripped symbol
    filtered_pair = None
    for pair in crypto_pairs:
        pair_symbol = pair['symbol']
        if pair_symbol == stripped_symbol:
            debug_messages(app,f"Quote pair: {pair}")
            filtered_pair = pair
            break
    
    # Check if the symbol was found
    if filtered_pair is None:
        return None

    currency_pair_id = filtered_pair['id']

    debug_messages(app,f"Sending price: {price}")

    orders = None

    while True:
        if orders and 'created_at' in orders:
            # Log the order info
            break

        if stock_type == 'buy':
            # Place a Market order
            if stock_position == 'market':
                orders = order_buy_crypto_by_quantity(
                    symbol=stripped_symbol,
                    _id=currency_pair_id,
                    quantity=quantity,
                    timeInForce='gtc',
                    jsonify=True
                )
            else:
                # Place a Limit order
                orders = order_buy_crypto_limit(
                    symbol=stripped_symbol,
                    quantity=quantity,
                    limitPrice=price,
                    _id=currency_pair_id,
                    timeInForce='gtc',
                    jsonify=True
                )
        else:
            # Place a Market order
            if stock_position == 'market':
                orders = order_sell_crypto_by_quantity(
                    symbol=stripped_symbol,
                    _id=currency_pair_id,
                    quantity=quantity,
                    timeInForce='gtc',
                    jsonify=True
                )
            else:
                # Place a Limit order
                orders = order_sell_crypto_limit(
                    symbol=stripped_symbol,
                    quantity=quantity,
                    limitPrice=price,
                    _id=currency_pair_id,
                    timeInForce='gtc',
                    jsonify=True
                )

    return orders


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