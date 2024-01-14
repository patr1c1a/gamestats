from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from game_stats.views import *

urlpatterns = [
   re_path(r"^players/?$", PlayerListCreate.as_view(), name="player-list-or-create"),
   re_path(r"^players/(?P<pk>\d+)/?$", PlayerRetrieveUpdateDestroy.as_view(), name="player-by-id"),
   re_path(r"^stats/?$", StatListCreate.as_view(), name="stat-list-or-create"),
   re_path(r"^stats/(?P<pk>\d+)/?$", StatRetrieveUpdateDestroy.as_view(), name="stat-by-id"),
   re_path(r"^games/?$", GameListCreate.as_view(), name="game-list-or-create"),
   re_path(r"^games/(?P<pk>\d+)/?$", GameRetrieveUpdateDestroy.as_view(), name="game-by-id"),
   re_path(r"^stats/ranking/?$", StatRankingView.as_view(), name="top-10-scores"),
   re_path(r"^users/?$", UserListCreate.as_view(), name="user-list-or-create"),
   re_path(r"^users/(?P<pk>\d+)/?$", UserRetrieveUpdateDestroy.as_view(), name="user-by-id"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
