from flask import Flask, request, jsonify
import random
import requests
import hazelcast

app = Flask(__name__)

# Підключення до кластера Hazelcast
hz = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["127.0.0.1:5701"])
# Отримання черги з повідомленнями з Hazelcast
messages_queue = hz.get_queue("queue").blocking()

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    # Випадкове вибір портів для логування та повідомлень
    logging_port = random.randint(5001, 5003)
    message_port = random.randint(5005, 5006)

    if request.method == 'GET':
        # Відправка GET-запитів до сервісів логування та повідомлень
        response_logging = requests.get(f'http://127.0.0.1:{logging_port}/data', timeout=5)
        response_logging.raise_for_status() # Перевірка статусу відповіді
        response_message = requests.get(f'http://127.0.0.1:{message_port}/data').text
        return jsonify({'Message data': response_message, 'Log data': response_logging.text})
    elif request.method == 'POST':
         # Обробка POST-запиту з отриманим повідомленням
        message = request.get_data().decode('utf-8')
        messages_queue.offer(message) # Додавання повідомлення до черги в Hazelcast
        log_data = {"msg": message}
        print(f'Sending log to logging-service on port {logging_port}')
        response = requests.post(f'http://127.0.0.1:{logging_port}/data', json=log_data)
        response.raise_for_status() # Перевірка статусу відповіді
        return f'Message sent to queue and logged: {message}'

if __name__ == '__main__':
    print('Starting facade service on port 5000')
    app.run(debug=True, port=5000)
