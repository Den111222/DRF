import csv
import datetime
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from games.models import GameModel, GamerModel, GamerLibraryModel
from games.serializers import GameModelSerializer, GamerModelSerializer, UserSerializer
from rest_framework.response import Response


#Это загрузка базы из файла .csv, для того чтобы можно было работать дальше
def upload_data(request):
    with open('vgsales.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                _, created = GameModel.objects.get_or_create(
                    name=row[1],
                    platform=row[2],
                    year=datetime.date(int(row[3]), 1, 1),
                    genre=row[4],
                    publisher=row[5],
                    na_sales=row[6],
                    eu_sales=row[7],
                    jp_sales=row[8],
                    other_sales=row[9],
                    global_sales=row[10],
                )
            except:
                pass
    return HttpResponse("Done!")

class AllView(ListView):
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.all()

class FilterView(ListView):
    template_name = 'gamemodel_list.html'                                   #
    queryset = GameModel.objects.filter(
        ~Q(name__startswith="Ab") | ~Q(name__startswith="Ad") | ~Q(
            name__startswith="Mat"))
    # ##Оставил, как вариант
    # queryset = GameModel.objects.filter(na_sales__gt=30)

def relation_filter_view(request):
    data = GamerLibraryModel.objects.filter(gamer__email__contains="a")
    print(data[0].gamer.email)
    return HttpResponse(data.order_by())

class ExcludeView(ListView):
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.exclude(name__contains="Hitman")

class OrderByView(ListView):
    template_name = 'gamemodel_list.html'
    # Сортировка по году начиная с большего
    queryset = GameModel.objects.exclude(name__contains="Hitman").order_by(
        '-year')
    ##Альтернативный вариант
    # queryset = GameModel.objects.exclude(name__contains="Hitman").order_by('year').reverse()

class UnionView(ListView):
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.filter(name="Hitman").union(
        GameModel.objects.filter(name="Tetris"))

class NoneView(ListView):
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.none()

class ValuesView(ListView):
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.filter(name="Tetris").values("name", "platform", "year")

def date_view(request):
    data = GameModel.objects.dates(field_name='year', kind='day')
    return HttpResponse(data)

def get_view(request):
    data = GameModel.objects.get(pk=1)
    return HttpResponse(data)

def create_view(request):
    myself = GamerModel()
    myself.email = "admin@admin.com"
    myself.nickname = "SomeRandomNicknameSave"
    myself.save()
    my_friend = GamerModel.objects.filter(pk=1)
    my_friend.update(nickname="MySecondNickname")
    return HttpResponse(my_friend)

@csrf_exempt                        #для использования проверки доступа (аутентификации)
@api_view(["POST"])                 #чтобы использовать функцию как view
@permission_classes((AllowAny,))    #для использования разграничения прав (авторизации)
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please username and password'})
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid data'})

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)

class CreateUser(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

@csrf_exempt
@api_view()
#Пример представлений (View), через функцию
def view_function(request):
    print(request.data)
    return Response(request.data)

#Пример представлений (View), через класс
class ClassAPIView(APIView):
    def get(self, request):
        return Response({'class': 'some_class_data'})
    def post(self, request):
        print(request.data)
        return Response(request.data)

#Пример набора представлений (ViewSet)
class ViewSetAPIView(viewsets.ViewSet):
    queryset = GameModel.objects.filter(id__lte=10)
    def list(self, request):
        serializer = GameModelSerializer(self.queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = GameModelSerializer(user)
        return Response(serializer.data)

class GameViewSet(viewsets.ModelViewSet):
    queryset = GameModel.objects.all().order_by('-year')
    serializer_class = GameModelSerializer

class GamerViewSet(viewsets.ModelViewSet):
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer

#Пример использования генератора, для создания пользователя
class MyCreateAPIView(CreateAPIView):
    serializer_class = GamerModelSerializer

#Пример использования генератора, для получения данных пользователей
class MyRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUser,)     #ограничение разрешений, только для админов
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer

#Пример использования генератора, для изменения данных пользователей
class MyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer
