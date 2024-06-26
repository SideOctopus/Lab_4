import requests

def send_post(message):
    # Функція для відправки POST-запиту з повідомленням на сервер
    response = requests.post('http://localhost:5000/data', data=message.encode('utf-8'))
    print(f'Response from server: {response.text}') # Виведення відповіді сервера

def send_get():
    # Функція для відправки GET-запиту для отримання повідомлень від сервера
    response = requests.get('http://localhost:5000/data')
    print(f'Response from server: {response.text}') # Виведення відповіді сервера


def main_menu():
    while True:
        print("\n*** Client Menu ***")
        print("1. Send POST request with a message")
        print("2. Send GET request to retrieve messages")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            message = input("Enter the message to send: ")
            send_post(message)
        elif choice == '2':
            send_get()
        elif choice == '3':
            print("Exiting the client...")
            break
        else:
            print("Invalid choice. Please choose from 1 to 3.")

if __name__ == '__main__':
    main_menu()
