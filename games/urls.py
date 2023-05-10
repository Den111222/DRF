from django.urls import path, include
from rest_framework import routers
from games import views

router = routers.SimpleRouter()
router.register(r'game', views.GameViewSet)
router.register(r'gamer', views.GamerViewSet)
router.register(r'view-set', views.ViewSetAPIView)

urlpatterns = [
    path('upload/', views.upload_data, name='upload'),
    path('filter/', views.FilterView.as_view(), name='filter'),
    path('relation-filter/', views.relation_filter_view,
         name='relation_filter'),
    path('exclude/', views.ExcludeView.as_view(), name='exclude'),
    path('orderby/', views.OrderByView.as_view(), name='orderby'),
    path('', views.AllView.as_view(), name='all'),
    path('union/', views.UnionView.as_view(), name='union'),
    path('none/', views.NoneView.as_view(), name='none'),
    path('values/', views.ValuesView.as_view(), name='values'),
    path('dates/', views.date_view, name='dates'),
    path('get/', views.get_view, name='get'),
    path('create/', views.create_view, name='create'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('function/', views.view_function, name='function_view'),
    path('class/', views.ClassAPIView.as_view(), name='class_view'),
    path('generic/', views.MyCreateAPIView.as_view(), name='generic'),
    path('retrieve/<int:pk>', views.MyRetrieveAPIView.as_view(), name='retrieve'),
    path('retrieve-update/<int:pk>', views.MyRetrieveUpdateAPIView.as_view(), name='retrieve_update'),
    path('api-login', views.user_login),
    path('create-user', views.CreateUser.as_view()),
]
