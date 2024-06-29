from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from options import *
from stocks import *
from crypto import *
import logging,json
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Configure logging
logging.basicConfig(level=logging.INFO)

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
        # Attempt to parse JSON data
        try:
            data = request.json
        except Exception:
            data = json.loads(request.data)

        #app.logger.info(f"Received webhook data: {data}")

        # Process the data received from TradingView webhook
        stockOrOptions = data.get('option')
        stock_position = data.get('position')
        stock_creditOrdebit = data.get('cord')
        stock_symbol = data.get('symbol')
        stock_quantity = data.get('qtity')
        stock_type = data.get('type')
        stock_price = data.get('price')

        # Log extracted values
        #app.logger.info(f"Position: {stock_position}, Cord: {stock_creditOrdebit}, Symbol: {stock_symbol}, Quantity: {stock_quantity}, Type: {stock_type}, Price: {stock_price}")
        if stockOrOptions == 'stocks':
            print("Heading to the Stock Function")
        
        if stockOrOptions == 'crypto':
            app.logger.info("Heading to the Crypto Function")
            crypto_robinhood(stock_symbol,stock_quantity,stock_price,app)

        # Run the function with the received data
        result = process_stock_data(stock_position, stock_creditOrdebit, 
                                    stock_symbol, stock_quantity, 
                                    stock_type, stock_price)

        # Emit the result to WebSocket clients
        socketio.emit('trading_data', {'symbol': stock_symbol, 'price': stock_price, 'result': result})

        return jsonify({'message': 'Webhook received', 'result': result}), 200
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_stock_data(stock_position, stock_creditOrdebit, 
                                    stock_symbol, stock_quantity, 
                                    stock_type, stock_price):
    
    app.logger.info(f"Processing data for {stock_symbol} with price {stock_price}")
    find_options(position=str(stock_position), cOrd=str(stock_creditOrdebit), symbol=str(stock_symbol), 
                 qtity=str(stock_quantity), price=str(stock_price), 
                 type=str(stock_type), ac=f'{config.get("ACCOUNTINFO", "accountid")}')
    
    result = f"Processed data for {stock_symbol} at price {stock_price}"
    return result

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
