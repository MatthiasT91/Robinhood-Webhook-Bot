from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import logging

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    if request.content_type != 'application/json':
        app.logger.error('Unsupported Media Type: Content-Type must be application/json')
        return jsonify({'error': 'Unsupported Media Type: Content-Type must be application/json'}), 415

    try:
        data = request.json
        app.logger.info(f"Received webhook data: {data}")

        # Process the data received from TradingView webhook
        stock_symbol = data.get('symbol')
        stock_price = data.get('price')

        # Run the function with the received data
        result = process_stock_data(stock_symbol, stock_price)

        # Emit the result to WebSocket clients
        socketio.emit('trading_data', {'symbol': stock_symbol, 'price': stock_price, 'result': result})

        return jsonify({'message': 'Webhook received', 'result': result}), 200
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_stock_data(symbol, price):
    # Dummy function to process stock data
    # Replace this with your actual processing logic
    app.logger.info(f"Processing data for {symbol} with price {price}")
    result = f"Processed data for {symbol} at price {price}"
    return result

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
