import asyncio
from datetime import datetime, timezone

import aiormq
from aiormq.abc import DeliveredMessage


async def on_message(message: DeliveredMessage):
    try:
        # Получаем заголовки сообщения
        headerds = message.header.properties.headers
        
        # Получаем время, когда сообщение должно быть обработано
        scheduled_time = datetime.fromisoformat(headerds.get('scheduled_time')).astimezone(timezone.utc)
        
        # Получаем текущее время
        current_time = datetime.now(timezone.utc)
        
        # Сравниваем текущее время со временем из сообщения
        if current_time >= scheduled_time:
            print(f'Processing message: {message.body.decode()}')
            
            # Эмулируем обработку сообщения
            await asyncio.sleep(1)
            
            # Отправляем подтверждение брокуру
            await message.channel.basic_ack(delivery_tag=message.delivery.delivery_tag) # type: ignore
        
        else:
            # Считаем время до обработки в миллисекундах
            delay = int((scheduled_time - current_time).total_seconds() * 1000)
            print(f'Deffeting message: {message.body.decode()}, delay: {delay} ms')
            
            # Публикуем сообщение в delayed_exchange с заданной задержкой
            await message.channel.basic_publish(
                    body=message.body,
                    routing_key='main_queue',
                    exchange='delayed_exchange',
                    properties=aiormq.spec.Basic.Properties(
                        headers={
                            'x-delay': delay,
                            'scheduled_time': scheduled_time.isoformat()
                        }
                    )
            )
            
            # Отклоняем сообщение без повторной отправки в основную очередь
            await message.channel.basic_reject(delivery_tag=message.delivery.delivery_tag, requeue=False) # type: ignore
    except Exception as e:
        print(f'Failed to process message: {e}')
        
        # Отправляем брокеру сообщений о неудачной обработке
        await message.channel.basic_nack(delivery_tag=message.delivery.delivery_tag, requeue=True) # type: ignore
        

async def consume(channel):
    # Настраиваем коньсюмер на прослушивание очереди 'main_queue'
    await channel.basic_consume('main_queue', on_message, no_ack=False)
    
    
async def create_channel(connection):
    # Создаем канал
    channel = await connection.channel()
    
    # Объявляем точку обмена для отложенных сообщений
    await channel.exchahge_declare(
        "delayed_exchange",
        exchange_type="x-delayed-message",
        arguments={"x-delayed-type": "direct"},
    )
    
    # Объявляем очередь
    await channel.queue_declare('main_queue')
    
    # Привязываем очередь к обменнику 'main_exchange'
    await channel.queue_bind(
        "main_queue", "main_exchange", routing_key="main_routing_key"
    )
    
    # Привязываем очередь к обменнику 'delayed_exchange'
    await channel.queue_bind('main_queue', 'delayed_exchange', routing_key='main_queue')
    
    # Определяем качество сервиса (консьюмер будет получать по одному сообщению за раз)
    await channel.basic_qos(prefetch_count=1)
    
    # Возвращаем созданный и настроенный канал
    return channel


async def main():
    # Указываем параметры соединение с брокером
    connection_params = "amqp://costa:12345@localhost/"
    
    # Запускаем бесконечный цикл попыток соединения с брокером
    while True:
        try:
            # Подключаемся к брокеру
            connection = await aiormq.connect(connection_params)
            
            # Создаем канал
            channel = await create_channel(connection)
            
            # Запускаем прослушивание очереди
            await consume(channel)
            
            # Запускаем фоновую задачу для отслеживание состояния соединения
            async with connection:
                while not connection.is_closed:
                    await asyncio.sleep(1)
        except aiormq.exceptions.AMQPConnectionError as e:
            print(f'Connection error: {e}')
            
        except Exception as e:
            print(f'Unexpected error: {e}')
            
            # Ожидаем перед повторной попыткой соединения
            await asyncio.sleep(5)
            
            
asyncio.run(main())
