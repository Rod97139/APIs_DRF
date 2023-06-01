from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
 
from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, ProductDetailSerializer, ProductListSerializer, ArticleSerializer, CategoryListSerializer

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
 
 
class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()
 
    serializer_class = CategoryListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = CategoryDetailSerializer
 
    def get_queryset(self):
        return Category.objects.filter(active=True)
 
    
class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()
 
    serializer_class = ProductListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = ProductDetailSerializer
 
    def get_queryset(self):
    # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
class ArticleViewset(ReadOnlyModelViewSet):
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
    # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Article.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
 
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
        # Nous avons simplement à appliquer la permission sur le viewset
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        return Category.objects.all()
    

class AdminArticleViewset(ModelViewSet):
 
    serializer_class = ArticleSerializer
 
    queryset =  Article.objects.all()
        
 
# class CategoryAPIView(APIView):
 
#     def get(self, *args, **kwargs):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
    
# class ProductAPIView(APIView):
 
#     def get(self, *args, **kwargs):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)