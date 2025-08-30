import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from warehouse import urls as warehouse_urls
from users import urls as users_urls
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            warehouse_urls.websocket_urlpatterns + users_urls.websocket_urlpatterns
        )
    ),
})