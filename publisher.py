import asyncio
import aiormq
#

async def publish():
    # Подключение к rabbitmq
    connection = await aiormq.connect(
        "amqp://costa:12345@localhost/"
    )
    
    # Создание канала
    channel = await connection.channel()
    
    # Объявление точки обмена (создается, если не существует)
    await channel.exchange_declare("test_exchange", exchange_type='direct')
    
    # Отправка сообщения в exchange
    await channel.basic_publish(
        body="Hi hi hi из RabbitMQ!".encode("utf-8"),
        exchange="test_exchange",
        routing_key="test_routing_key"
    )
    
    # Закрытие соединения
    await connection.close()
    

asyncio.run(publish())
    