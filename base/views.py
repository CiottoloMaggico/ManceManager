import datetime

from django.views.generic import TemplateView, DetailView, FormView, UpdateView
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Client, Activity, Parcel, Category
from .forms import ActivityForm, ClientForm, QuarterFormSet, ParcelForm, CategoryForm
from .filters import ActivityFilter, ClientFilter, CategoryFilter

class ClientListView(FormView):
    template_name = 'base/client_list.html'
    form_class = ClientForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(ClientListView, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        filter = ClientFilter(self.request.GET, queryset=Client.objects.all())
        context['pricing'] = Client.global_price_hour_rate()
        context['filter'] = filter
        context['clients'] = filter.qs
        return context

class CategoryListView(CreateView):
    template_name = 'base/category_list_manage.html'
    success_url = '/categories'
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        filter = CategoryFilter(self.request.GET, queryset=Category.objects.all())
        context['filter'] = filter
        context['categories'] = filter.qs
        return context

class ClientDetailView(FormView):
    template_name = 'base/client_detail.html'
    form_class = ActivityForm

    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        form.save()
        return super(ClientDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        client = Client.objects.prefetch_related('activities').get(id=self.kwargs['pk'])
        filter = ActivityFilter(self.request.GET, queryset=client.activities.all())
        context['filter'] = filter
        context['client'] = client
        context['worked_hours'] = client.get_hours(filter.qs)
        context['activities'] = filter.qs.order_by('-date')
        context['parcels'] = client.parcels.all().order_by('-year')
        return context

    def get_initial(self):
        initial = super(ClientDetailView, self).get_initial()
        initial['client'] = get_object_or_404(Client, id=self.kwargs['pk'])
        return initial

class ActivityDetailView(DetailView):
    template_name = 'base/activity_detail.html'
    model = Activity

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data()
        context['client'] = get_object_or_404(Client, id=self.kwargs['id'])
        return context

class ParcelCreateView(FormView):
    template_name = 'base/parcel_create_update.html'
    form_class = ParcelForm

    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        parcel_model = form.save(commit=False)
        form_set = QuarterFormSet(self.request.POST, instance=parcel_model)
        if form_set.is_valid():
            parcel_model.save()
            form_set.save()

        return super(ParcelCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ParcelCreateView, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(Client, id=self.kwargs['pk'])
        context['form'] = ParcelForm(
            initial={
                'client':context['client'],
            }
        )
        context['parcel'] = QuarterFormSet()
        return context


class ParcelUpdateView(UpdateView):
    model = Parcel
    form_class = ParcelForm
    template_name = 'base/parcel_create_update.html'

    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        context = super(ParcelUpdateView, self).get_context_data()
        current_parcel = get_object_or_404(Parcel, id=self.kwargs['pk'])
        context['parcel_model']=current_parcel
        context['client'] = get_object_or_404(Client, id=self.kwargs['id'])
        context['form'] = ParcelForm(initial={'client':context['client']}, instance=current_parcel)
        context['parcel'] = QuarterFormSet(instance=current_parcel)
        context['update'] = True
        return context

    def form_valid(self, form):
        parcel_model = form.save(commit=False)
        form_set = QuarterFormSet(self.request.POST, instance=parcel_model)
        if form_set.is_valid():
            parcel_model.save()
            form_set.save()

        return super(ParcelUpdateView, self).form_valid(form)


class BaseDeleteView(DeleteView):
    template_name = 'base/delete_view.html'

class ClientDeleteView(BaseDeleteView):
    model = Client
    success_url = reverse_lazy('client_list')

    def get_context_data(self, **kwargs):
        context = super(ClientDeleteView, self).get_context_data()
        context['back_url'] = f'/'
        return context

class CategoryDeleteView(BaseDeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data()
        context['back_url'] = f'/categories'
        return context

class BackToClientDetailDeleteView(BaseDeleteView):
    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        context = super(BackToClientDetailDeleteView, self).get_context_data()
        context['back_url'] = f'/client/{self.kwargs["id"]}/'
        return context

class ActivityDeleteView(BackToClientDetailDeleteView):
    model = Activity

class ParcelDeleteView(BackToClientDetailDeleteView):
    model = Parcel