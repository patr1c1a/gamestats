from .models import Player, Stat, Game
from .serializers import PlayerSerializer, StatSerializer, GameSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render


class CustomPagination(PageNumberPagination):
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


class PlayerList(generics.ListCreateAPIView):
    """
    API endpoint that allows players to be viewed or created.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = CustomPagination


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single player to be viewed, updated, or deleted.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameList(generics.ListCreateAPIView):
    """
    API endpoint that allows games to be viewed or created.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = CustomPagination


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single game to be viewed, updated, or deleted.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class StatList(generics.ListCreateAPIView):
    """
    API endpoint that allows stats to be viewed or created.
    """
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    pagination_class = CustomPagination


class StatDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single stat to be viewed, updated, or deleted.
    """
    queryset = Stat.objects.all()
    serializer_class = StatSerializer


class StatRankingView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get_top_scores(self):
        top_scores = Stat.objects.order_by('-score')[:10]
        serializer = StatSerializer(top_scores, many=True)
        return serializer.data

    def get(self, request):
        top_scores = self.get_top_scores()

        # Check if the request accepts HTML content
        if request.accepted_renderer.format == "html":
            context = {'ranking_data': top_scores}
            return render(request, 'report.html', context)

        # Return JSON response for other cases
        return Response(top_scores)
