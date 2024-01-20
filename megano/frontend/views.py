from django.views.generic import TemplateView, ListView
from shopapp.models import Item





class TemplateView(TemplateView):
    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
