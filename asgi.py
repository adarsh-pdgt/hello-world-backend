import os

from hello_world.messages.apis import websocket_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

async def application(scope, receive, send):
    await websocket_application(scope, receive, send)
