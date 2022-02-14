from django.urls import re_path

from .views import VideoConferenceView

websocket_urlpatterns = [
    re_path(r'', VideoConferenceView.as_asgi())
]