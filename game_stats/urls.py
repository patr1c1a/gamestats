from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from game_stats.views import *

urlpatterns = [
   path("players/", PlayerList.as_view()),
   path("players/<int:pk>/", PlayerDetail.as_view()),
   path("stats/", StatList.as_view()),
   path("stats/<int:pk>/", StatDetail.as_view()),
   path("games/", GameList.as_view()),
   path("games/<int:pk>/", GameDetail.as_view()),
   path("stats/ranking/", StatRankingView.as_view(), name='stat-ranking'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
