from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from options import *
from stocks import *
from crypto import *
import logging,json
import configparser


app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Configure logging
logging.basicConfig(level=logging.INFO)


def read_config(config_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_path)
    settings = {}
    for key, value in config.items("SETTINGS"):
        settings[key] = value
    return settings


def write_orders_to_file(orders, filename='orders.txt'):
    try:
        with open(filename, 'a') as file:
            json.dump(orders, file)
            file.write('\n')  # Add a newline after each JSON object
        print(f"Orders successfully written to {filename}")
        return
    except Exception as e:
        print(f"Error writing orders to {filename}: {e}")
        return


def clean_value(value):
    """Remove curly braces and return value as string."""
    return str(value).strip('{}')


@app.route('/health', methods=['GET'])
def health_check():
    app.logger.info('Health check endpoint called')
    return jsonify({'status': 'Running'}), 200


@socketio.on('connect')
def handle_connect():
    app.logger.info('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    app.logger.info('Client disconnected')


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = None

        if not request.data:
            raise ValueError("Empty payload received")

        try:
            data = request.get_json()
            if data is None:
                raise ValueError("Invalid JSON received")
        except Exception as e:
            raise ValueError(f"Error parsing JSON: {str(e)}")

        settings = read_config()
            
        stockOrOptions = data.get('option', None)
        stock_position = data.get('position', None)
        stock_creditOrdebit = data.get('cord', None)
        stock_symbol = data.get('symbol', None)
        stock_quantity = data.get('qtity', None)
        stock_option_type = data.get('option_type', None)
        stock_type = data.get('type', None)
        stock_price1 = data.get('price1', None)
        stock_price2 = data.get('price2', None)
        stock_expiration = data.get('expiration', None)
        stock_strike = data.get('strike', None)

        if stockOrOptions == 'options':
            #if stock_type == 'stop_limit':
            #    find_options(position=str(stock_position), cOrd=str(stock_creditOrdebit), symbol=str(stock_symbol), 
            #         qtity=str(stock_quantity), price1=str(stock_price1), price2=str(stock_price2), strike=str(stock_strike),
            #         expiration=str(stock_expiration), option_type=str(stock_option_type), type=str(stock_type), ac='120853833', app=None)

            result = find_options(position=str(stock_position), cOrd=str(stock_creditOrdebit), symbol=str(stock_symbol), 
                 qtity=str(stock_quantity), price1=str(stock_price1), price2=str(stock_price2), 
                 strike=str(stock_strike), expiration=str(stock_expiration), 
                 option_type=str(stock_option_type), type=str(stock_type), app=app, settings=settings)
            if result:
                write_orders_to_file([result])
            else:
                app.logger.info("Waiting for valid order creation...")
   
        if stockOrOptions == 'crypto':
            results = crypto_robinhood(stock_symbol, stock_quantity, stock_price1, 
                        stock_type, stock_position, 
                        settings, app)
            if results:
                write_orders_to_file([results])
            else:
                app.logger.info("Waiting for valid order creation...")

        if stockOrOptions == 'stocks':
            resultss = find_stocks(position=stock_position,symbol=stock_symbol,
                        qtity=stock_quantity,price1=stock_price1,
                        type=stock_type,app=app,settings=settings)
            if resultss:
                write_orders_to_file([resultss])
            else:
                app.logger.info("Waiting for valid order creation...")
        
        data = {}
        stockOrOptions = None
        stock_position = None
        stock_creditOrdebit = None
        stock_symbol = None
        stock_quantity = None
        stock_option_type = None
        stock_type = None
        stock_price1 = None
        stock_price2 = None
        stock_expiration = None
        stock_strike = None

        app.logger.info("Waiting for more messages...")
        return jsonify({'message': 'Webhook received and processed successfully'}), 200
        
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
