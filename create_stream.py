import asyncio

import nats
from nats.aio.client import Client
from nats.js.api import StreamConfig
from nats.js.client import JetStreamContext


async def main():
    # Подключаемся к NATS серверу
    nc: Client = await nats.connect('nats://127.0.0.1:4222') # type:ignore
    # Получаем JetStream контекст
    js: JetStreamContext = nc.jetstream()
    
    # Настройка стрима с заданными параметрами
    stream_config = StreamConfig(
        name='SocialMediaStream',
        description=None,
        subjects=[
            'social_media.user.signup',
            'social_media.post.created',
            'social_media.post.like',
            'social_media.comment.*'
        ],
        retention='limits', # Политика удержания
        max_consumers=-1, # Количество потребителей (в данном случае, неограниченное)
        max_msgs=-1, # Количество сообщений (в данном случае, неограниченное)
        max_bytes=300 * 1024 * 1024, # 300 MiB
        discard='old', # Политика удаления сообщений (сначала старые)
        max_age=None, # Возраст сообщений (неограниченный)
        max_msgs_per_subject=-1, # Количество сообщений на сабджект (неограниченное)
        max_msg_size=10 * 1024 * 1024, # 10 MiB
        storage='file', # Тип хранения данных (на жестком диске)
        num_replicas=1, # Количество реплик стрима
        no_ack=False, # Требуется явное подтверждение обработки
        template_owner=None, # Можно указать название шаблона, которому принадлежит стрим
        duplicate_window=2 * 60, # 2 минуты
        placement=None, # Правила размещения стрима на узлах кластера
        mirror=None, # Параметр, определяющий будет ли стрим зеркалом другого стрима
        sources=None, # Используется для агрегации данных из нескольких стримов в один
        sealed=False, # Стрим скрыт для добавления новых данных
        deny_delete=False, # Разрешение удалять сообщений
        deny_purge=False, # Разрешение очищать сабджекты или весь стрим
        allow_rollup_hdrs=False, # Запрет на "сворачивание сообщений"
        republish=None, # Настройка перебуликации сообщений в другие темы
        subject_transform=None, # Позволяет изменять тему сообщений на основе правил
        allow_direct=True, # Разрешение получать сообщения без создания консьюмера
        mirror_direct=None, # Настройка разрешения публикации в зеркальный стрим без консьюмера
        compression=None, # Настройка сжатия сообщений в стриме
        metadata=None # Метаданные стрима
    )
    
    await js.add_stream(stream_config)
    
    print('Stream "SocialMediaStream" created successfully')
    
    
asyncio.run(main())
