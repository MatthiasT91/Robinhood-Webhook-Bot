from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json  # Assuming TradingView sends JSON data
        print(f"Received webhook data: {data}")
        socketio.emit('trading_data', data)  # Broadcast data via WebSocket if needed
        return jsonify({'message': 'Webhook received'}), 200
    except Exception as e:
        print(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Running'}), 200

if __name__ == '__main__':
    socketio.run(app)
