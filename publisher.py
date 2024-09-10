import asyncio
from datetime import datetime

import nats


async def main():
    # Подключаемся к серверу NATS
    nc = await nats.connect('nats://127.0.0.1:4222')
    
    # Задержка в секундах
    delay = 5
    
    # Сообщение для отправки
    message = 'Hello from Python-publisher'
    
    # Заголовки
    headers = {
        'Tg-Delayed-Msg-Timestamp': str(datetime.now().timestamp()),
        'Tg-Daleyed-Msg-Delay': str(delay)
    }
    
    # Сабджект, в который отправляются сообщени
    subject = "aiogram.delayed.messages"
    
    # Publish msg to subject
    await nc.publish(subject=subject, payload=message.encode(encoding='utf-8'), headers=headers)
    
    # Print in console mgs about successfull publish
    print(f"Message '{message}' with headers '{headers}' published in subject '{subject}'")

    # Close connection
    await nc.close()
    
    
asyncio.run(main())    
