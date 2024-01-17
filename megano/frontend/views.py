from django.views.generic import TemplateView, ListView
from shopapp.models import Item


class HomeView(TemplateView):
    template_name = "frontend/index.html"


class ShopListView(ListView):
    model = Item
    context_object_name = 'items'


class ItemDetailView(TemplateView):
    template_name = "frontend/product.html"


class TemplateView(TemplateView):
    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
