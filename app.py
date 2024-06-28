from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    # Process data received from TradingView webhook
    # Example: forward data to WebSocket clients
    socketio.emit('trading_data', data, namespace='/')
    return jsonify({'message': 'Webhook received'}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True)

    ## Add some thdown here
