import websockets
import asyncio

# хранилище, которое хранит все сокеты клиентов
all_clients = set()


async def send_message(message: str):
    """
    Функция для отправки сообщений всем пользователям
    :param message:
    :return:
    """
    for client in all_clients:
        await client.send(message)


async def new_client_connected(client_socket: websockets.WebSocketClientProtocol, path: str):
    """
    Функция которая будет работать с каждым клиентом, получать от него сообщения
    :param client_socket: сокет клиента
    :param path: путь по которому клиент пришел
    """
    print('New client connected!')
    all_clients.add(client_socket)
    while True:
        # получение всех сообщений от клиента
        new_message = await client_socket.recv()
        print("New messages from a client: ", new_message)
        await send_message(message=new_message)


async def run_server():
    """
    Завпуск сервера, serve  принимает 3 аргумента
    - фу-ю callback(будет вызыватся при каждом подключении клиента)
    - хост
    - порт
    :return:
    """
    await websockets.serve(new_client_connected, 'localhost', 12345)


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_server())
    event_loop.run_forever()
