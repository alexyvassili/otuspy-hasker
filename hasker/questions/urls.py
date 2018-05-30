from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new, name='new_questions'),
    path('q/<int:uid>/', views.question, name='question'),
    path('q/<str:tagword>/', views.tag_search, name='tag_search'),
    path('ask', views.ask, name='ask'),
    path('user', views.profile, name='user_profile'),
    path('search', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('set_default_avatar/', views.set_default_avatar, name='set_default_avatar'),
    path('q/<int:uid>/like/', views.like_question, name='like_question'),
    path('q/<int:uid>/dislike/', views.dislike_question, name='dislike_question'),
    path('q/answer/<int:ans_uid>/like/', views.like_answer, name='like_answer'),
    path('q/answer/<int:ans_uid>/dislike/', views.dislike_answer, name='dislike_answer'),
    path('q/answer/<int:ans_uid>/is_solution/', views.set_answer_as_solution, name='set_answer_as_solution'),
    path('ajax/tags/push/', views.send_all_tags, name="send_all_tags")
]
