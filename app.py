from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from options import *
from stocks import *
from crypto import *
import logging,json


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
            
        stockOrOptions = data.get('option')
        stock_position = data.get('position')
        stock_creditOrdebit = data.get('cord')
        stock_symbol = data.get('symbol')
        stock_quantity = data.get('qtity')
        stock_type = data.get('type')
        stock_price = data.get('price')
        
        if stockOrOptions == 'options' or stockOrOptions == 'stocks':
            app.logger.info("Heading to the Stock Function")
            print("Heading to the Stock Function")
            # Run the function with the received data
            result = process_stock_data(stock_position, stock_creditOrdebit, 
                                        stock_symbol, stock_quantity, 
                                        stock_type, stock_price)
            # Emit the result to WebSocket clients
            socketio.emit('trading_data', {'symbol': stock_symbol, 'price': stock_price, 'result': result})
            # Reset variables to ensure a clean slate for the next iteration
            data = {}
            stockOrOptions = None
            stock_position = None
            stock_creditOrdebit = None
            stock_symbol = None
            stock_quantity = None
            stock_type = None
            stock_price = None
        
        elif stockOrOptions == 'crypto':
            app.logger.info("Heading to the Crypto Function")
            creating_order = crypto_robinhood(stock_symbol, stock_quantity, stock_price, stock_type, stock_position, app)
            app.logger.info(f"After Buying: {creating_order}")
            if creating_order:
                order_details = extract_order_details(creating_order)
                discord_message(order_details)
                app.logger.info(order_details)
                # Reset variables to ensure a clean slate for the next iteration
                data = {}
                stockOrOptions = None
                stock_position = None
                stock_creditOrdebit = None
                stock_symbol = None
                stock_quantity = None
                stock_type = None
                stock_price = None
            else:
                app.logger.info("Waiting for valid order creation...")
        app.logger.info("Waiting for more messages...")
        return jsonify({'message': 'Webhook received and processed successfully'}), 200
        
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_stock_data(stock_position, stock_creditOrdebit, 
                                    stock_symbol, stock_quantity, 
                                    stock_type, stock_price):
    
    app.logger.info(f"Processing data for {stock_symbol} with price {stock_price}")
    find_options(position=str(stock_position), cOrd=str(stock_creditOrdebit), symbol=str(stock_symbol), 
                 qtity=str(stock_quantity), price=str(stock_price), 
                 type=str(stock_type), ac='120853833')
    
    result = f"Processed data for {stock_symbol} at price {stock_price}"
    return result

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
