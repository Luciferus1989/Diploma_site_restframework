from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import request

from .views import (CategoriesAPIView,
                    CatalogListView,
                    ItemDetailView,
                    PopularItemAPIView,
                    LimitedItemAPIView,
                    FeedBackPost,
                    BannerAPIView,
                    ProfileAPIView,
                    TagView,
                    BasketAPIView,
                    OrderAPIView,
                    OrderDetailAPIView,
                    PaymentAPIView,
                    LoginApiView, LogoutApiView, RegisterApiView, SalesAPIView,
                    )
from django.conf import settings
from django.conf.urls.static import static

app_name = 'api'

urlpatterns = [
    # path('about/', TemplateView.as_view(template_name="frontend/about.html")),
    path('basket', BasketAPIView.as_view(), name='basket_api'),
    path('catalog/', CatalogListView.as_view(), name='catalog_api'),
    path('catalog/<int:id>/', CatalogListView.as_view(), name='catalogid_api'),
    path('categories/', CategoriesAPIView.as_view(), name='categories_api'),
    path('tags/', TagView.as_view(), name='tags_api'),
    path('orders', OrderAPIView.as_view(), name='orders_api'),
    # path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html")),
    path('order/<int:id>', OrderDetailAPIView.as_view(), name='orders_details_id_api'),
    path('orders/<int:id>', OrderDetailAPIView.as_view(), name='orders_id_api'),
    path('payment/<int:id>', PaymentAPIView.as_view(), name='payment_id_api'),
    path('payment-someone/', PaymentAPIView.as_view(), name='payment_someone_api'),
    path('product/<int:id>/', ItemDetailView.as_view(), name='api-product-detail'),
    path('products/popular/', PopularItemAPIView.as_view(), name='api-products-popular'),
    path('products/limited/', LimitedItemAPIView.as_view(), name='api-products-limited'),
    path('product/<int:pk>/reviews', FeedBackPost.as_view(), name='api-products-reviews'),
    path('banners/', BannerAPIView.as_view(), name='api-banners'),
    path('profile', ProfileAPIView.as_view(), name='api-profile'),
    path('profile/password', ProfileAPIView.as_view(), name='api-password'),
    path('profile/avatar', ProfileAPIView.as_view(), name='api-password'),
    path('sales/', SalesAPIView.as_view(), name='api-sale'),
    path('sign-in', LoginApiView.as_view(), name='api-login'),
    path('sign-out', LogoutApiView.as_view(), name='api-logout'),
    path('sign-up', RegisterApiView.as_view(), name='api-register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

