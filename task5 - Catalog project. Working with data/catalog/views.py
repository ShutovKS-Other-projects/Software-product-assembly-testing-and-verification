from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView

from .models import SSD, Interface, FormFactor


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
        form_factor = self.params.get('form_factor')
        min_price = self.params.get('min_price')
        max_price = self.params.get('max_price')
        sort_by = self.params.get('sort', 'brand')  # По умолчанию сортируем по бренду

        if search_query:
            queryset = queryset.filter(
                Q(brand__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(sku__icontains=search_query)
            )
        if interface:
            queryset = queryset.filter(interface__name=interface)
        if form_factor:
            queryset = queryset.filter(form_factor__name=form_factor)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Сортировка
        if sort_by in ['brand', 'model', 'price', 'capacity_gb', 'read_speed', 'write_speed', 'warranty_years']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('brand', 'model')  # По умолчанию

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['params'] = self.params
        context['interfaces'] = Interface.objects.all()
        context['form_factors'] = FormFactor.objects.all()
        context['sort_options'] = [
            ('brand', 'По бренду'),
            ('model', 'По модели'),
            ('price', 'По цене'),
            ('capacity_gb', 'По объему'),
            ('read_speed', 'По скорости чтения'),
            ('write_speed', 'По скорости записи'),
            ('warranty_years', 'По гарантии')
        ]
        return context


class SSDDetailView(DetailView):
    model = SSD
    template_name = "catalog/detail.html"


class AboutView(TemplateView):
    template_name = "catalog/about.html"
