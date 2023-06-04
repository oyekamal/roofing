from django.shortcuts import render, get_object_or_404, redirect

from .forms import ServiceRequestForm, UserProfileForm, ServiceProviderForm
from .models import UserProfile, ServiceRequest, Offer, ServiceProvider
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.

class ServiceProviderDetailView(DetailView):
    model = ServiceProvider
    template_name = 'service/service_provider_detail.html'
    
class ServiceProviderListView(ListView):
    model = ServiceProvider
    template_name = 'service/service_provider_list.html'

class ServiceProviderCreateView(LoginRequiredMixin, CreateView):
    model = ServiceProvider
    form_class = ServiceProviderForm
    template_name = 'service/service_provider_form.html'
    success_url = '/service_providers/'
    
    
    def dispatch(self, request, *args, **kwargs):
        if ServiceProvider.objects.filter(user=self.request.user).exists():
            return redirect(reverse('service:service_provider_detail', args=[self.request.user.serviceprovider.pk]))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ServiceProviderUpdateView(LoginRequiredMixin, UpdateView):
    model = ServiceProvider
    form_class = ServiceProviderForm
    template_name = 'service/service_provider_form.html'
    success_url = '/service_providers/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ServiceProviderDeleteView(DeleteView):
    model = ServiceProvider
    template_name = 'service/service_provider_confirm_delete.html'
    success_url = '/service_providers/'


def home(request):

    return render(request, "service/home.html")

class OfferDetailView(DetailView):
    model = Offer
    template_name = 'service/offer_detail.html'
 
def service_request_list(request):
    service_requests = ServiceRequest.objects.filter(client=request.user)
    return render(request, "service/service_request_list.html", {"service_requests": service_requests})


class ServiceRequestUpdateView(UpdateView):
    model = ServiceRequest
    fields = ['service_area', 'service_type', 'description']
    template_name = 'service/service_request_update.html'

    def get_success_url(self):
        return reverse_lazy('service:service_request_list')


class ServiceRequestDeleteView(DeleteView):
    model = ServiceRequest
    success_url = reverse_lazy('service:service_request_list')
    template_name = 'service/service_request_delete.html'

class ServiceRequestDetailView(DetailView):
    model = ServiceRequest
    template_name = 'service/service_request_detail.html'

def service_request(request):
    if request.method == "GET":
        form = ServiceRequestForm()
        mydict = {
            "form": form,
        }
        return render(request, "service/service_request_form.html", context=mydict)
    else:
        try:
            request.POST._mutable = True
            request_data = request.POST.copy()
            request_data["client"] = request.user.id if request.user.is_authenticated else None
            request_data["status"] = "Open"
            form = ServiceRequestForm(request_data)

            if form.is_valid():
                form.save()
                return render(
                    request, "service/service_request_form.html", {
                        "form": form, "success": True}
                )
            else:
                print(form.errors)
        except Exception as e:
            print(e)
            return render(request, "service/service_request_form.html", {"form": form})
        return render(request, "service/service_request_form.html", {"form": form})
