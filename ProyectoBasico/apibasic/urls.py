
from django.urls import path, include
from apibasic import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', views.ArticleViewSet, basename='article')
router2 = DefaultRouter()
router2.register('artigen', views.ArticleGenericViewSet, basename='artigen')
router3 = DefaultRouter()
router3.register('artimodel', views.ModalArticleViewSet, basename='artimodel')

urlpatterns = [
    path('api/', views.article_list),
    path('apidetail/<int:pk>',views.article_detail), #pk tomara el valor en el url
    path('apiview/', views.ArticleAPIView_list.as_view()), #Cuando se usa classes en las views en urls va una funcion as_view()
    path('apiviewdetail/<int:id>', views.ArticleAPIView_detail.as_view()),
    path('apigeneric/<int:id>', views.GenericAPIView.as_view()),
    #path para el viewset
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>', include(router.urls)),
    path('viewsetgeneric/', include(router2.urls)),
    path('viewsetgeneric/<int:pk>', include(router2.urls)),
    #ModelVIWESET
    path('modelviewset/<int:pk>', include(router3.urls)),
    path('modelviewset/', include(router3.urls)),
]