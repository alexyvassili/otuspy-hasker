from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new, name='new_questions'),
    path('q', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('user', views.profile, name='user_profile'),
    path('search', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('set_default_avatar/', views.set_default_avatar, name='set_default_avatar')
]
