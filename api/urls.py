from django.urls import path
from .views import main, RegisterUser, UserDataView, LoginUser, UploadDocuments

urlpatterns = [
    path('main/', main),
    path('register/',RegisterUser.as_view()),
    path('login/',LoginUser.as_view()),
    path('showuser/',UserDataView.as_view()),
    path('uploadDocs/',UploadDocuments.as_view())
]