from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route('/test')
def hello():
    return "Hello World!"

@app.route('/start_process')
def start_proc():
    data = {"message": "Process Started"}
    return jsonify(data)

@app.route('/stop_process')
def stop_proc():
    data = {"message": "Process Stopped"}
    return jsonify(data)

@app.route('/command', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    
    if command == 'start':
        # Implement your start logic here
        return jsonify({'status': 'START Command received'})
    
    elif command == 'stop':
        # Implement your stop logic here
        return jsonify({'status': 'STOP Command received'})
    
    elif command == 'restart':
        # Implement your restart logic here
        return jsonify({'status': 'RESTART Command received'})

    else:
        return jsonify({'error': 'Unknown command'}), 400
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)