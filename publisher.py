import asyncio
import nats


async def main():
    # Подключаемся к NATS серверу
    nc = await nats.connect("nats://127.0.0.1:4222")
    
    # Сообщение для отправки
    message = 'Hello hello from Python!'
    
    # Сабджект, в которой отправляется сообщение
    subject = 'my.first.subject'
    
    # Публикуем сообщение в указанный сабджект
    await nc.publish(subject=subject, payload=message.encode())
    
    print(f'Message "{message}" published in subject "{subject}"')

    # Закрываем соединение
    await nc.close()
    
    
asyncio.run(main())
