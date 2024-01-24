import django_filters
import logging
from rest_framework import serializers
from shopapp.models import Item, ItemImage, Category, FeedBack, Tag, Specification, Basket, Order, Sale, SaleItem
from myauth.models import CustomUser
from decimal import Decimal

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['fullName', 'email', 'phone', 'avatar', 'first_name', 'last_name']

    def get_fullName(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_avatar(self, obj):
        if obj.avatar:
            return {
                'src': obj.avatar.url,
                'alt': 'Avatar Image'
            }
        return None


class ItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    minPrice = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    maxPrice = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    freeDelivery = django_filters.BooleanFilter(field_name='free_delivery')
    available = django_filters.BooleanFilter(field_name='available')
    category = django_filters.NumberFilter(field_name='category')

    class Meta:
        model = Item
        fields = ['name', 'price', 'freeDelivery', 'available', 'category']


class ItemImageSerializer(serializers.ModelSerializer):
    src = serializers.ImageField()

    class Meta:
        model = ItemImage
        fields = ('src', 'description')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class FeedBackSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format='%d-%m-%Y')

    class Meta:
        model = FeedBack
        fields = ['item', 'author', 'email', 'text', 'rate', 'date']


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['name', 'value']


class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True)
    reviews = FeedBackSerializer(many=True, read_only=True, source='feedbacks')
    rating = serializers.SerializerMethodField()
    title = serializers.CharField(source='name')
    tags = TagSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id',
                  "category",
                  'title',
                  'price',
                  'count',
                  'date',
                  'description',
                  'free_delivery',
                  'images',
                  'tags',
                  'reviews',
                  'specifications',
                  'rating']

    def get_rating(self, obj):
        return obj.calculate_overall_rating()

    def get_reviews(self, obj):
        return obj.get_feedbacks_count()


class BasketItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    quantity = serializers.IntegerField(source='quantity')

    class Meta:
        model = Basket
        fields = ['item', 'quantity']

    def to_representation(self, instance):
        item_representation = ItemSerializer(instance.item).data
        sale_price = instance.item.price * (1 - Decimal(instance.item.discount) / 100)
        return {
            'id': item_representation['id'],
            'category': item_representation['category'],
            'price': sale_price,
            'count': instance.quantity,
            'date': item_representation['date'],
            'title': item_representation['title'],
            'description': item_representation['description'],
            'freeDelivery': item_representation['free_delivery'],
            'images': item_representation['images'],
            'tags': item_representation['tags'],
            'reviews': item_representation['reviews'],
            'rating': item_representation['rating'],
        }


class CustomProductSerializer(serializers.Serializer):

    class Meta:

        fields = ['id', 'category', 'price', 'count', 'date', 'title', 'description',
                  'freeDelivery', 'images', 'tags', 'reviews', 'rating']


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    products = BasketItemSerializer(many=True, read_only=True, source='basket_set')
    deliveryType = serializers.SerializerMethodField()
    paymentType = serializers.CharField(source='payment_type')
    totalCost = serializers.DecimalField(max_digits=10, decimal_places=2, source='total_amount')

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'customer', 'deliveryType', 'paymentType',
                  'status', 'city', 'address', 'products', 'totalCost']

    def get_deliveryType(self, obj):
        has_paid_delivery = any(item.free_delivery is False for item in obj.items.all())
        return 'free' if not has_paid_delivery else 'paid'

    def to_representation(self, instance):
        formatted_data = {
            'id': instance.id,
            'createdAt': instance.created_at.strftime('%Y-%m-%d %H:%M'),
            'fullName': instance.customer.get_fullName(),
            'email': instance.customer.email,
            'phone': instance.customer.phone,
            'deliveryType': self.get_deliveryType(instance),
            'paymentType': instance.payment_type,
            'totalCost': instance.total_amount,
            'status': instance.status,
            'city': instance.city,
            'address': instance.address,
            'products': BasketItemSerializer(instance.basket_set.all(), many=True).data,
        }

        return formatted_data


class SalesItemSerializer(serializers.ModelSerializer):
    items = ItemSerializer()

    class Meta:
        model = SaleItem
        fields = ['items']

    def to_representation(self, instance):
        item_representation = self.fields['items'].to_representation(instance.item)
        sale_price = instance.item.price * (1 - Decimal(instance.sale.discount) / 100)
        sale_representation = {
            'id': item_representation['id'],
            'dateFrom': instance.sale.date_from.strftime('%d-%m'),
            'dateTo': instance.sale.date_to.strftime('%d-%m'),
            'salePrice': sale_price,
        }

        return {**item_representation, **sale_representation}


class SubcategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def get_image(self, obj):
        return {'src': obj.image.url, 'alt': 'Image alt string'} if obj.image else None

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        if subcategories:
            return SubcategorySerializer(subcategories, many=True).data
        return []


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def get_image(self, obj):
        return {'src': obj.image.url, 'alt': 'Image alt string'} if obj.image else None

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return SubcategorySerializer(subcategories, many=True).data


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar']
