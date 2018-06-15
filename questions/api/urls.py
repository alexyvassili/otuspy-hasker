from django.urls import path

from questions.api import api_schema
from questions.api import views

#               ###  DRF URL's ###
urlpatterns = [
    path('', api_schema.schema_view),
    path('v1.0/', api_schema.schema_view),
    path('v1.0/questions/', views.questions_list),
    path('v1.0/questions/<int:uid>/', views.question_detail),
    path('v1.0/questions/<int:uid>/answers/', views.question_answers),
    path('v1.0/trending/', views.trending),
    path('v1.0/search/', views.search),
    ]
