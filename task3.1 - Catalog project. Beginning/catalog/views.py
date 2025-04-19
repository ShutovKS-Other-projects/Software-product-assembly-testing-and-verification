from django.db.models import Q
from django.views.generic import ListView, TemplateView, DetailView

from .models import SSD


class HomeView(ListView):
    model = SSD
    template_name = "catalog/home.html"
    context_object_name = "ssd_list"
    paginate_by = 48

    def get_queryset(self):
        queryset = super().get_queryset()
        self.params = self.request.GET.copy()

        search_query = self.params.get('search')
        interface = self.params.get('interface')
        min_price = self.params.get('min_price')
        max_price = self.params.get('max_price')

        if search_query:
            queryset = queryset.filter(
                Q(brand__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(sku__icontains=search_query)
            )

        if interface:
            queryset = queryset.filter(interface=interface)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['params'] = self.params
        return context


class SSDDetailView(DetailView):
    model = SSD
    template_name = "catalog/detail.html"


class AboutView(TemplateView):
    template_name = "catalog/about.html"
