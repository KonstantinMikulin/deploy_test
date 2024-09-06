import asyncio
from asyncio import CancelledError

import nats
from nats.aio.msg import Msg


# Функция обработчик полученных сообщений
async def message_handler(msg: Msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received message '{data}' from subject '{subject}'")
    
    
async def main():
    # Подключаемся к NATS серверу
    nc = await nats.connect('nats://127.0.0.1:4222')
    
    # Сабджект для подписки
    subject = 'my.first.subject'
    
    # Подписываемся на указанный сабджект
    await nc.subscribe(subject=subject, cb=message_handler)
    
    print(f"Subscribed to sunject '{subject}'")

    # Создаем future для поддержания соединения открытым
    try:
        await asyncio.Future()
    except CancelledError:
        pass
    finally:
        # Закрываем соединение
        await nc.close()
        
        
asyncio.run(main())
