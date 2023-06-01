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
      
    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError('Price must be greater than 1')
        return value

    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Inactive product')
        return value
        
class ProductListSerializer (ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'ecoscore']
        
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
            'id','date_created', 'date_updated', 'name', 'description'
        ]
    
    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Category already exists')
        return value
    
    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
        # Levons une ValidationError si ça n'est pas le cas
            raise serializers.ValidationError('Name must be in description')
        return data
    

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
        