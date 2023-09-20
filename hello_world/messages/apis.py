# import socketio

async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event['type'] == 'websocket.connect':
            await send({
                'type': 'websocket.accept'
            })

        if event['type'] == 'websocket.disconnect':
            break

        if event['type'] == 'websocket.receive':
            if event['text'] == 'ping':
                await send({
                    'type': 'websocket.send',
                    'text': 'pong!'
                })

# sio = socketio.Client()
#
# @sio.event
# def connect():
#     print('connection established')
#
# @sio.event
# def my_message(data):
#     print('message received with ', data)
#     sio.emit('my response', {'response': 'my response'})
#
# @sio.event
# def disconnect():
#     print('disconnected from server')
#
# sio.connect('http://localhost:3001')
# sio.wait()
