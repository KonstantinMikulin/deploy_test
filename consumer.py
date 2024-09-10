import asyncio
from asyncio import CancelledError
from datetime import datetime, timedelta, timezone

import nats
from nats.aio.msg import Msg


# Function for processing received msgs
async def on_message(msg: Msg):
    # Get timestamp and delay from headers
    sent_time = datetime.fromtimestamp(
        float(msg.headers.get("Tg-Delayed-Msg-Timestamp")), tz=timezone.utc #type:ignore
    )
    delay = int(msg.headers.get("Tg-Daleyed-Msg-Delay"))  # type:ignore

    # Check if it is time for msg processing
    if sent_time + timedelta(seconds=delay) > datetime.now().astimezone():
        # If not time for processing, calculate how much time left before processing
        new_delay = (sent_time + timedelta(seconds=delay) - datetime.now().astimezone()).total_seconds()
        
        # Send nak with time of delay
        await msg.nak(delay=new_delay)
    else:
        # If it is time for processing, print info in console
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received message '{data}' from subject '{subject}'")
        
        await msg.ack()
        
        
async def main():
    # Connect to NATS server
    nc = await nats.connect('nats://127.0.0.1:4222')
    # Get JetStream context
    js = nc.jetstream()
    
    # Subject for subscription
    subject = "aiogram.delayed.messages"
    
    # Stream for subscription
    stream = 'delayed_messages_aiogram'
    
    # Subscribe for the stream
    await js.subscribe(
        subject=subject,
        stream=stream,
        cb=on_message,
        durable='dealayed_message_consumer',
        manual_ack=True
    )
    
    print(f"Subscribed for subject '{subject}'")
    
    # Create 'future' for keeping connection open
    try:
        await asyncio.Future()
    except CancelledError:
        pass
    finally:
        # Close connection
        await nc.close()
        
        
asyncio.run(main())
