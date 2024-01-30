from .models import Player, Stat, Game
from .serializers import PlayerSerializer, StatSerializer, GameSerializer, UserSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import AllowAny, IsAdminUser
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
    Allows players to be listed or created.
    TODO: user can only associate a player to themselves. Admins can associate players to any user.
    """
    queryset = Player.objects.all().order_by("id")
    serializer_class = PlayerSerializer
    pagination_class = CustomPagination


class PlayerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows a single player to be viewed, updated or deleted.
    TODO: Only admins or user associated with the player can PUT or PATCH.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_permissions(self):
        """
        Only allow admin users to delete.
        """
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return []


class GameListCreate(generics.ListCreateAPIView):
    """
    Allows games to be listed or created.
    """
    queryset = Game.objects.all().order_by("id")
    serializer_class = GameSerializer
    pagination_class = CustomPagination


class GameRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows a single game to be viewed, updated or deleted.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        """
        Only allow admin users to delete, put or patch.
        """
        if self.request.method in ["DELETE", "PUT", "PATCH"]:
            return [IsAdminUser()]
        return []

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Adds a custom message to the response content.
        """
        if response.status_code == 204 and request.method == "DELETE":
            response.data = {"message": "Game deleted successfully"}
        elif response.status_code == 200 and request.method in ["PUT", "PATCH"]:
            response.data = {"message": "Game updated successfully"}
        return super().finalize_response(request, response, *args, **kwargs)


class StatListCreate(generics.ListCreateAPIView):
    """
    Allows stats to be listed or created.
    """
    queryset = Stat.objects.all().order_by("id")
    serializer_class = StatSerializer
    pagination_class = CustomPagination


class StatRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows a single stat to be viewed, updated or deleted.
    """
    queryset = Stat.objects.all()
    serializer_class = StatSerializer

    def get_permissions(self):
        """
        Only allow admin users to delete, put or patch.
        """
        if self.request.method in ["DELETE", "PUT", "PATCH"]:
            return [IsAdminUser()]
        return []


class StatRankingView(APIView):
    """
    Allows listing the stats with top 10 scores.
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer, CustomCSVRenderer]
    serializer_class = StatSerializer

    def get_top_scores(self):
        """
        Obtains the top 10 stats according to highest scores.
        """
        top_scores = Stat.objects.order_by("-score")[:10]
        serializer = StatSerializer(top_scores, many=True)
        data = serializer.data

        # Flatten the player data and remove unused game data
        for item in data:
            item["player"] = item["player"]["nickname"]
            item.pop("id", None)
            item.pop("creation_date", None)
            item.pop("game", None)

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
            response["Content-Disposition"] = 'attachment; filename="top_scores.csv"'
            return response

        # Return JSON response for other cases
        else:
            return Response(top_scores)


class UserListCreate(generics.ListCreateAPIView):
    """
    Allows users to be listed or created.
    """
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Applies permissions according to the method used (GET: needs user to be authenticated, POST: users can be
        created by anyone).
        """
        if self.request.method == "GET":
            return [IsAdminUser()]
        elif self.request.method == "POST":
            return [AllowAny()]
        return []


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows a single user to be retrieved, updated or deleted.
    TODO: Only admins and logged in user can PUT or PATCH.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Only allow admin users to delete.
        """
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return []
