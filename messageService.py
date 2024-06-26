from flask import Flask, jsonify, request
import hazelcast
import argparse
import threading

app = Flask(__name__)
message_list = []

def queue_event():
    while True:
        item = messages_queue.take()
        message_list.append(item)
        print("Отримано повідомлення з черги: ", str(item))

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # Обробка GET-запиту: повертає всі отримані повідомлення у вигляді рядка через новий рядок
        return '\n'.join(message_list)
    elif request.method == 'POST':
        # Обробка POST-запиту: отримання повідомлення з JSON тіла запиту, додавання його до списку повідомлень і виведення у консоль підтвердження отримання
        msg = request.json['msg']
        message_list.append(msg)
        print(f'Отримано повідомлення через POST: {msg}')
        return f'Повідомлення отримано: {msg}', 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    # Підключення до кластера Hazelcast та отримання блокуючої черги повідомлень
    hz = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["127.0.0.1:5701"])
    messages_queue = hz.get_queue("queue").blocking()

    # Запуск окремого потоку для обробки подій черги
    event_thread = threading.Thread(target=queue_event)
    event_thread.start()

    print(f'Запуск сервісу повідомлень на порту {args.port}')
    app.run(debug=True, port=args.port)
