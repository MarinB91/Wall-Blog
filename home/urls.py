from django.urls import path
from . import views


urlpatterns = [
    # General URLs
    path('', views.messages, name='messages'),
    path('messages/top_message', views.top_message, name='top_messages'),
    path('messages/<str:title>', views.individual_message, name='individual_message'),
    path('delete/<str:title>', views.delete, name='deletion'),

    # Auth URLs
    path('registration_login', views.login_page, name='registration_login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),

    # Voting URLs
    path('upvote/<str:name>', views.vote, name='upvote'),
    path('downvote/<str:name>', views.vote, name='downvote'),
]
