from django.urls import path, include

from Test.models import Vote
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('simple-viewset', views.SimpleViewSet)


route = DefaultRouter()
route.register('polls', views.PollViewSet, basename='polls')

urlpatterns = [
    
    #path('', views.simple),
    path('simple', views.SimpleAPI.as_view()),
    
    path('simple/<int:id>', views.SimpleAPI.as_view()),
    
    path('simple-generics', views.SimpleGenerics.as_view()),
    path('simple-generics/<int:id>', views.SimpleGenericsUpdate.as_view()),
    
    path('', include(router.urls)),
    
    path('poll', views.poll, name='poll'),
    path('poll/<int:id>', views.poll_detail, name='poll-detail'),
    
    path('pol', views.PollList.as_view()),
    path('pol/<int:pk>/', views.PollDetail.as_view()),
    
    path('p/', views.PollListSerial.as_view()),
    path('p/<int:id>', views.PollCreateSerial.as_view()),
    
    path('vote/', views.VoteCreate.as_view()),
    path('choices/', views.ChoiceList.as_view()),
    
    #### new urls
    path('poll/<int:pk>/choices', views.ChoiceList.as_view()),
    path('poll/<int:pk>/choices/<int:choice_pk>/votes', views.VoteCreate.as_view()),
    
    path('user/', views.UserCreate.as_view()),
    path('login/', views.LoginView.as_view()),
    
    
] + route.urls


