from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from shop.views import CategoryAPIView, ProductAPIView

from shop.views import CategoryViewset, ProductViewset, ArticleViewset, AdminCategoryViewset, AdminArticleViewset

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArticleViewset, basename='article')
router.register('admin/category', AdminCategoryViewset, basename='admin-category')
router.register('admin/article', AdminArticleViewset, basename='admin-article')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/category/', CategoryAPIView.as_view()),
    # path('api/product/', ProductAPIView.as_view()),
    path('api/', include(router.urls)),
]

# # urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls')),
# ]
