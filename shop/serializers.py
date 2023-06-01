from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
 
from shop.models import Category, Product, Article

class ArticleSerializer(ModelSerializer):
 
    class Meta:
        model = Article
        fields = ['id', 'name',
                   'date_created',
                'date_updated',
                'product',
                'price',

                   ]
        
class ProductListSerializer (ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id','date_created', 'date_updated', 'name', 'category'
        ]
class ProductDetailSerializer(ModelSerializer):
    
    articles = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name',
                   'date_created',
                'date_updated',
                'category',
                'articles'
                   ]
    def get_articles(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.articles.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ArticleSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
         

class CategoryListSerializer (ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id','date_created', 'date_updated', 'name'
        ]
class CategoryDetailSerializer(ModelSerializer):
  # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits sont multiples pour une catégorie
    # products = ProductSerializer(many=True)
    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
    products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name',
                   'date_created',
                   'date_updated',
                   'products'
                   ]
    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductDetailSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
        