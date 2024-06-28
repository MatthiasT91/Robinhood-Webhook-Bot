from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')  # Adjust async_mode as needed

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        # Process incoming data
        socketio.emit('trading_data', data)  # Example: broadcast data via WebSocket
        return jsonify({'message': 'Webhook received'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors gracefully

if __name__ == '__main__':
    socketio.run(app)
