from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from game_stats import views

urlpatterns = [
   path("players/", views.PlayerList.as_view()),
   path("players/<int:pk>/", views.PlayerDetail.as_view()),
   path("stats/", views.StatList.as_view()),
   path("stats/<int:pk>/", views.StatDetail.as_view()),
   path("games/", views.GameList.as_view()),
   path("games/<int:pk>/", views.GameDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
