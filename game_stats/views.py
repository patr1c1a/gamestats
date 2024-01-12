from .models import Player, Stat, Game
from .serializers import PlayerSerializer, StatSerializer, GameSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.models import User
from .renderers import CustomCSVRenderer


class CustomPagination(PageNumberPagination):
    """
    Adds pagination to endpoints.
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "results": data,
            }
        )


class PlayerListCreate(generics.ListCreateAPIView):
    """
    Allows players to be viewed or created.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = CustomPagination


class PlayerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows a single player to be viewed, updated, or deleted.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameListCreate(generics.ListCreateAPIView):
    """
    Allows games to be viewed or created.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = CustomPagination


class GameRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows a single game to be viewed, updated, or deleted.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class StatListCreate(generics.ListCreateAPIView):
    """
    Allows stats to be viewed or created.
    """
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    pagination_class = CustomPagination


class StatRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows a single stat to be viewed, updated, or deleted.
    """
    queryset = Stat.objects.all()
    serializer_class = StatSerializer


class StatRankingView(APIView):
    """
    Allows listing the stats with top 10 scores.
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer, CustomCSVRenderer]

    def get_top_scores(self):
        """
        Obtains the top 10 stats according to highest scores.
        """
        top_scores = Stat.objects.order_by("-score")[:10]
        serializer = StatSerializer(top_scores, many=True)
        data = serializer.data

        # Flatten the player data and remove unused game data
        for item in data:
            item['player'] = item['player']['nickname']
            item.pop('id', None)
            item.pop('creation_date', None)
            item.pop('game', None)

        return data if data else []

    def get(self, request):
        """
        Implements GET HTTP method for html and json requests, as well as serve the csv download feature.
        """
        top_scores = self.get_top_scores()

        # Check if the request accepts HTML content
        if request.accepted_renderer.format == "html":
            context = {"ranking_data": top_scores}
            return render(request, "report.html", context)

        # CSV export
        elif request.accepted_renderer.format == "csv":
            response = Response(top_scores, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="top_scores.csv"'
            return response

        # Return JSON response for other cases
        else:
            return Response(top_scores)


class UserListCreate(generics.ListCreateAPIView):
    """
    Allows users to be listed or created.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Applies permissions according to the method used (GET: needs user to be authenticated, POST: users can be
        created by anyone).
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [AllowAny()]
        return []


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows users to be retrieved, updated, or deleted.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

