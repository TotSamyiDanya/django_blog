from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('like/', views.like, name='like'),
    path('comment/', views.comment, name='comment'),
    path('personal/', views.personal, name='personal'),
    path('create/', views.create, name='create'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('editor/', views.editor, name='editor'),
    path('editor/<int:post_id>', views.editor, name='editor'),
    path('poll/', views.PollClass.as_view(), name='poll'),
    path('complete/', views.complete_poll, name='complete'),
    path('post/<int:post_id>', views.post, name='post')
]
