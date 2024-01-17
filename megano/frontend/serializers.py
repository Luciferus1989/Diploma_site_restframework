# import django_filters
# from rest_framework import serializers
# from shopapp.models import Item, ItemImage
#
#
# class ItemFilter(django_filters.FilterSet):
#     title = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
#     minPrice = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
#     maxPrice = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
#     freeDelivery = django_filters.BooleanFilter(field_name='free_delivery')
#     available = django_filters.BooleanFilter(field_name='available')
#     category = django_filters.NumberFilter(field_name='category')
#
#     class Meta:
#         model = Item
#         fields = []
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         print(self.form.data)
#
#
# class ItemImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ItemImage
#         fields = ('src', 'description')
#
#
# class ItemSerializer(serializers.ModelSerializer):
#     images = ItemImageSerializer(many=True)
#     reviews = serializers.SerializerMethodField()
#     rating = serializers.SerializerMethodField()
#     title = serializers.CharField(source='name')
#
#     class Meta:
#         model = Item
#         fields = ['id',
#                   'title',
#                   'price',
#                   'count',
#                   'date',
#                   'description',
#                   'free_delivery',
#                   'images',
#                   'tags',
#                   'reviews',
#                   'rating']
#
#     def get_reviews(self, obj):
#         return obj.get_feedbacks_count()
#
#     def get_rating(self, obj):
#         return obj.get_average_rating()
#
#
# # class ItemSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Item
# #         fields = '__all__'
