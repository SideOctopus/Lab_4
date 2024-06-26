from flask import Flask, request, jsonify
import argparse

app = Flask(__name__)
logs = []

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # Обробка GET-запиту: повертає усі логи у форматі JSON
        return jsonify(logs)
    elif request.method == 'POST':
        # Обробка POST-запиту: отримання логу з тіла запиту, запис до списку логів і виведення у консоль
        log = request.json['msg']
        logs.append(log)
        print(f'Received message via POST: {log}')  # Вивід отриманого повідомлення у консоль
        return f'Log recorded: {log}', 200  # Підтвердження запису логу з кодом статусу 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    print(f'Starting logging service on port {args.port}')  # Виведення інформації про запуск сервісу логування
    app.run(debug=True, port=args.port)
