from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from options import *
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

        app.logger.info(f"Received webhook data: {data}")

        # Process the data received from TradingView webhook
        stock_position = clean_value(data.get('position'))
        stock_creditOrdebit = clean_value(data.get('cord'))
        stock_symbol = data.get('symbol')
        stock_quantity = clean_value(data.get('qtity'))
        stock_type = clean_value(data.get('type'))
        stock_price = data.get('price')

        # Log extracted values
        app.logger.info(f"Position: {stock_position}, Cord: {stock_creditOrdebit}, Symbol: {stock_symbol}, Quantity: {stock_quantity}, Type: {stock_type}, Price: {stock_price}")


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
    # Dummy function to process stock data
    # Replace this with your actual processing logic
    find_options(position=stock_position, cOrd=stock_creditOrdebit, symbol=stock_symbol, 
                 qtity=stock_quantity, price=stock_price, 
                 type=stock_type, ac='120853833')
    
    result = f"Processed data for {stock_symbol} at price {stock_price}"
    return result

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
