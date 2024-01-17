from django.urls import path, include
from django.views.generic import TemplateView
from .views import HomeView, TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'frontend'



urlpatterns = [
    path('about/', TemplateView.as_view(template_name="frontend/about.html")),
    path('', HomeView.as_view(template_name="frontend/index.html"), name='index'),
    path('cart/', TemplateView.as_view(template_name="frontend/cart.html")),
    path('catalog/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('catalog/<int:id>/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html")),
    path('order-detail/<int:id>/', TemplateView.as_view(template_name="frontend/oneorder.html")),
    path('orders/<int:id>/', TemplateView.as_view(template_name="frontend/order.html")),
    path('payment/<int:id>/', TemplateView.as_view(template_name="frontend/payment.html")),
    path('payment-someone/', TemplateView.as_view(template_name="frontend/paymentsomeone.html")),
    path('product/<int:id>/', TemplateView.as_view(template_name="frontend/product.html")),
    path('profile/', TemplateView.as_view(template_name="frontend/profile.html")),
    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html")),
    path('sale/', TemplateView.as_view(template_name="frontend/sale.html")),
    path('sign-up/', TemplateView.as_view(template_name="frontend/signUp.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
