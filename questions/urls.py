from django.urls import path

from . import views, views_drf, api_schema


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new_questions'),
    path('q/<int:uid>/', views.question, name='question'),
    path('tag/<str:tagword>/', views.tag_search, name='tag_search'),
    path('ask/', views.ask, name='ask'),
    path('user/', views.profile, name='user_profile'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('invite/', views.invite, name='invite'),
    path('invite/generate/', views.invite_generate, name='invite_generate'),
    path('set_default_avatar/', views.set_default_avatar, name='set_default_avatar'),
    path('q/<int:uid>/like/', views.like_question, name='like_question'),
    path('q/<int:uid>/dislike/', views.dislike_question, name='dislike_question'),
    path('q/answer/<int:ans_uid>/like/', views.like_answer, name='like_answer'),
    path('q/answer/<int:ans_uid>/dislike/', views.dislike_answer, name='dislike_answer'),
    path('q/answer/<int:ans_uid>/is_solution/', views.set_answer_as_solution, name='set_answer_as_solution'),
    path('ajax/tags/push/', views.send_all_tags, name="send_all_tags"),

    #                 ###  DRF URL's ###

    path('api/', api_schema.schema_view),
    path('api/v1.0/', api_schema.schema_view),
    path('api/v1.0/questions/', views_drf.questions_list),
    path('api/v1.0/questions/<int:uid>/', views_drf.question_detail),
    path('api/v1.0/questions/<int:uid>/answers/', views_drf.question_answers),
    path('api/v1.0/trending/', views_drf.trending),
    path('api/v1.0/search/', views_drf.search),
]
