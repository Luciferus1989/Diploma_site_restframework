from datetime import datetime
from django.db.models import Avg, OuterRef, Subquery
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,)
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.views import APIView
from shopapp.models import Item, Category, FeedBack, Tag, Basket, Order
from myauth.models import CustomUser
from .serializers import (CategorySerializer,
                          ItemSerializer,
                          ItemFilter,
                          FeedBackSerializer,
                          UserSerializer,
                          ChangePasswordSerializer,
                          AvatarSerializer,
                          TagSerializer,
                          BasketItemSerializer,
                          OrderDetailSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response


class CategoriesAPIView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        categories = Category.objects.filter(parent_category__isnull=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class TagView(APIView):
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CatalogListView(ListAPIView):
    queryset = Item.objects.filter(archived=False)
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter
    ordering_fields = ['rating', 'price', 'reviews', 'date']
    ordering = 'date'
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        name = request.GET.get('filter[name]', '')
        min_price = float(request.GET.get('filter[minPrice]', 0))
        max_price = float(request.GET.get('filter[maxPrice]', 0))
        free_delivery = request.GET.get('filter[freeDelivery]')
        available = request.GET.get('filter[available]')
        category_id = request.GET.get('category', None)
        sort = request.GET.get('sort', 'date')
        sort_type = request.GET.get('sortType', 'dec')
        tags = request.GET.getlist('tags', [])

        queryset = Item.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if available == 'false':
            pass
        elif available == 'true':
            queryset = queryset.filter(available=True)
        if free_delivery == 'true':
            queryset = queryset.filter(free_delivery=True)
        if category_id:
            category_instance = Category.objects.get(id=category_id)
            category_serializer = CategorySerializer(instance=category_instance)
            subcategories = category_serializer.get_subcategories(category_instance)
            subcategory_ids = [subcategory['id'] for subcategory in subcategories]
            all_categories = [category_instance.id] + subcategory_ids
            queryset = queryset.filter(category__in=all_categories)
        if sort == 'rating':
            queryset = queryset.order_by('-rating' if sort_type == 'dec' else 'rating')
        elif sort == 'price':
            queryset = queryset.order_by('-price' if sort_type == 'dec' else 'price')
        elif sort == 'reviews':
            queryset = queryset.order_by('-review' if sort_type == 'dec' else 'review')
        elif sort == 'date':
            queryset = queryset.order_by('-date' if sort_type == 'dec' else 'date')

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serialized_items = self.get_serializer(page, many=True).data
        #     return self.get_paginated_response(serialized_items)

        serialized_items = self.get_serializer(queryset, many=True).data
        data = {
            'items': serialized_items,
            # 'currentPage': 1,
            # 'lastPage': 3,
        }
        # queryset = self.filter_queryset(queryset)
        # print(queryset.query)

        return Response(data, status=status.HTTP_200_OK)


class ItemDetailView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeedBackPost(APIView):
    def post(self, request, pk, *args, **kwargs):
        data = {'item': int(pk), **request.data, 'date': datetime.now()}

        serializer = FeedBackSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:

            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PopularItemAPIView(APIView):
    def get(self, request, format=None):
        avg_reviews = FeedBack.objects.filter(item=OuterRef('pk')).values('item').annotate(avg_reviews=Avg('rate')).values('avg_reviews')[:1]

        popular_products = Item.objects.annotate(
            avg_reviews=Subquery(avg_reviews)
        ).filter(
            avg_reviews__gt=5/2,
        ).order_by('-avg_reviews')[:10]

        serializer = ItemSerializer(popular_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LimitedItemAPIView(APIView):
    def get(self, request, format=None):
        limited_products = Item.objects.filter(count__lt=5)
        serializer = ItemSerializer(limited_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerAPIView(APIView):
    def get(self, request, format=None):
        serializer = ItemSerializer(Item.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if 'avatar' in data and len(data) == 1:
            user = request.user
            data = request.data
            serializer = AvatarSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif 'currentPassword' in data:
            serializer = ChangePasswordSerializer(data=data)
            if serializer.is_valid():
                if not user.check_password(serializer.validated_data.get("currentPassword")):
                    return Response({"currentPassword": ["Current password is not correct"]},

                                    status=status.HTTP_400_BAD_REQUEST)
                user.set_password(serializer.validated_data.get("newPassword"))
                user.save()
                return Response({"detail": "Password has been successfully changed"}, status=status.HTTP_200_OK)

            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif 'fullName' in data:
            full_name_parts = data['fullName'].split()
            first_name = full_name_parts[0] if full_name_parts else ''
            last_name = ' '.join(full_name_parts[1:]) if len(full_name_parts) > 1 else ''
            user.first_name = first_name
            user.last_name = last_name
            serializer = UserSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class BasketAPIView(APIView):
    serializer_class = BasketItemSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer_identifier = request.user.id
        else:
            customer_identifier = request.META.get('REMOTE_ADDR', None)
        order = Order.objects.filter(customer=customer_identifier, status='active').first()
        basket_items = Basket.objects.filter(order=order)
        serializer = self.serializer_class(basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        item = Item.objects.get(pk=request.data.get('id', 0))
        count = int(request.data.get('count', 0))
        if request.user.is_authenticated:
            customer_identifier = request.user.id
        else:
            customer_identifier = request.META.get('REMOTE_ADDR', None)

        order, created = Order.objects.get_or_create(customer=CustomUser.objects.get(id=customer_identifier),
                                                     status='active', total_amount=0)
        basket_item, created = Basket.objects.get_or_create(order=order, item=item)
        basket_item.quantity += count
        basket_item.save()

        serializer = self.serializer_class(basket_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        data = request.data
        item_id = data['id']
        count = data['count']
        user = request.user
        order = Order.objects.filter(customer=user, status='active').first()
        basket_item = Basket.objects.filter(order=order, item_id=item_id).first()
        if count < basket_item.quantity:
            basket_item.quantity -= count
            basket_item.save()
        else:
            basket_item.delete()
            remaining_items = Basket.objects.filter(order=order).exists()
            if not remaining_items:
                order.delete()
                serializer = BasketItemSerializer(remaining_items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        updated_basket_items = Basket.objects.filter(order=order)

        serializer = BasketItemSerializer(updated_basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        customer_identifier = request.user.id
        orders = Order.objects.filter(customer=customer_identifier)
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print('')
        customer_identifier = request.user.id
        order = Order.objects.filter(customer=customer_identifier, status='active').first()
        if order:
            order.status = 'pending'
            order.save()
            response_data = {'orderId': order.id}
            return Response(response_data, status=status.HTTP_200_OK)


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(self.queryset, id=kwargs[self.lookup_field])
        print(order)
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(self.queryset, id=kwargs[self.lookup_field])
        order.status = 'in process'
        order.save()
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentAPIView(APIView):
    def post(self, request, id):
        order_id = id
        payment_data = request.data
        try:
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)