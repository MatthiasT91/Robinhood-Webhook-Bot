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
    try:
        data = request.json
        app.logger.info(f"Received webhook data: {data}")
        socketio.emit('trading_data', data)
        return jsonify({'message': 'Webhook received'}), 200
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
