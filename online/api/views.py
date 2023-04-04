from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from store.models import Game
from .serializers import GameSerializer
from rest_framework.decorators import api_view
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework import filters
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
# class GetGameInfoView(generics.ListAPIView):
    
#     renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
#     serializer_class = GameSerializer
    
#     def get_queryset(self):
#         return Game.objects.filter(is_active=True)
    

class GetCategoryGameInfoView(generics.ListAPIView):
    
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    serializer_class = GameSerializer
    
    def get_queryset(self):
        category = self.kwargs['category']
        return Game.objects.filter(category__title=category.title())
    
    
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
class ResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'total'
    max_page_size = 4
    

class GetGameInfoView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    serializer_class = GameSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        from datetime import date
        queryset = Game.objects.all()
        release_date = self.request.query_params.get('release_date', None)
        print(release_date)
        if release_date is not None:
            print('Here')
            queryset = queryset.filter(release_date__year = int(release_date))
        return queryset
    
class GetGameInfoFilterView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['category__title',]
    
class GetGameInfoSearchView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    filter_backends = [rest_filters.SearchFilter]
    search_fields = ['name',]
    
class GetGameInfoOrderView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    filter_backends = [rest_filters.OrderingFilter]
    ordering_fields = ['name','release_date']

from store.models import Game

class GameFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Game
        fields = ['category__title',]


class GetGameInfoFilterSetView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = GameFilter


    
    
    # def get(self, request):
    #     # queryset = Game.objects.all()
    #     # print(request.query_params)
    #     # print(some_value)
    #     serializer_for_queryset = GameSerializer(
    #         instance=self.get_query_set, 
    #         many=True
    #     )
    #     return Response({"games": serializer_for_queryset.data})
    
    

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})