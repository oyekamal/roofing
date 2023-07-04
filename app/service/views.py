from django.shortcuts import render, get_object_or_404, redirect

from .forms import ServiceRequestForm, UserProfileForm, ServiceProviderForm, OfferForm, PreviousWorkForm
from .models import UserProfile, ServiceRequest, Offer, ServiceProvider, PreviousWork, Testimonials
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic import TemplateView

# Create your views here.

class PaypalReturnView(TemplateView):
    template_name = 'service/paypal_success.html'

class PaypalCancelView(TemplateView):
    template_name = 'service/paypal_cancel.html'

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
    testimonials = Testimonials.objects.all().order_by('-created_at')[:4]
    return render(request, "service/home.html", {"testimonials":testimonials})

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
    
class OfferAcceptedClient(DetailView):
    model = Offer

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        service_provider_email = self.object.service_provider.email

        accept_url = request.build_absolute_uri(reverse('service:accept_offer', kwargs={'pk': self.object.pk}))
        reject_url = request.build_absolute_uri(reverse('service:reject_offer', kwargs={'pk': self.object.pk}))
        cost_estimate = self.object.cost_estimate
        deducted_amount = float(cost_estimate) * 0.01

        context = {
            'accept_url': accept_url,
            'reject_url': reject_url,
            'deducted_amount': deducted_amount,
        }
        html_content = render_to_string('service/email_offer_template.html', context)

        send_mail(
            'Offer Accepted',
            '',
            settings.DEFAULT_FROM_EMAIL,
            [service_provider_email],
            fail_silently=False,
            html_message=html_content,
        )

        return super().get(request, *args, **kwargs)

class AcceptOffer(DetailView):
    model = Offer

    def get(self, request, *args, **kwargs):
        offer = self.get_object()
        if offer.status != "Pending":
            return HttpResponseForbidden("You cannot accept an offer which is not in 'Pending' status.")
        offer.status = "Accepted"
        # offer.save()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': offer.cost_estimate,
            'item_name': 'Offer',
            'invoice': str(offer.pk),
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('service:paypal-return')),
            'cancel_return': request.build_absolute_uri(reverse('service:paypal-cancel')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'service/paypal_form.html', {'form': form})

class RejectOffer(DetailView):
    model = Offer

    def get(self, request, *args, **kwargs):
        offer = self.get_object()
        if offer.status != "Pending":
            return HttpResponseForbidden("You cannot reject an offer which is not in 'Pending' status.")
        offer.status = "Rejected"
        offer.save()
        # Add any other actions you want to perform when the offer is rejected
        return super().get(request, *args, **kwargs)

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



def client_service_request_list(request):
    user = request.user
    if request.method == "GET":
        if ServiceProvider.objects.filter(user=user).exists():
            service_provider = ServiceProvider.objects.get(user=user)
            service_requests = ServiceRequest.objects.filter(service_area__in=service_provider.service_area.all())
            return render(request, 'service/client_service_request_list.html', {'service_requests': service_requests})
        else:
            # Handle cases where the user doesn't have a company account
            pass
        
        
def client_service_request_offer(request, service_request_id):
    service_request = get_object_or_404(ServiceRequest, id=service_request_id)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.service_provider = ServiceProvider.objects.get(user=request.user)
            offer.service_request = service_request
            offer.save()
            # Redirect to a success page or the same page with a success message
    else:
        form = OfferForm()
    return render(request, 'service/client_service_request_offer.html', {'service_request': service_request, 'form': form})



def previous_work_list(request, service_provider_id):
    service_provider = get_object_or_404(ServiceProvider, id=service_provider_id)
    previous_works = PreviousWork.objects.filter(service_provider=service_provider)
    return render(request, 'service/previous_work_list.html', {'previous_works': previous_works, 'service_provider': service_provider})

def previous_work_create(request, service_provider_id):
    service_provider = get_object_or_404(ServiceProvider, id=service_provider_id)
    if request.method == 'POST':
        form = PreviousWorkForm(request.POST, request.FILES)
        if form.is_valid():
            previous_work = form.save(commit=False)
            previous_work.service_provider = service_provider
            previous_work.save()
            return redirect(reverse('service:service_provider_detail', kwargs={'pk': service_provider.id}))
    else:
        form = PreviousWorkForm()
    return render(request, 'service/previous_work_form.html', {'form': form, 'service_provider': service_provider})

def previous_work_update(request, service_provider_id, previous_work_id):
    service_provider = get_object_or_404(ServiceProvider, id=service_provider_id)
    previous_work = get_object_or_404(PreviousWork, id=previous_work_id)
    if request.method == 'POST':
        form = PreviousWorkForm(request.POST, request.FILES, instance=previous_work)
        if form.is_valid():
            form.save()
            return redirect(reverse('service:service_provider_detail', kwargs={'pk': service_provider.id}))
    else:
        form = PreviousWorkForm(instance=previous_work)
    return render(request, 'service/previous_work_form.html', {'form': form, 'service_provider': service_provider})

def previous_work_delete(request, service_provider_id, previous_work_id):
    service_provider = get_object_or_404(ServiceProvider, id=service_provider_id)
    previous_work = get_object_or_404(PreviousWork, id=previous_work_id)
    previous_work.delete()
    # return redirect('service/previous_work_list', service_provider_id=service_provider.id)
    return redirect(reverse('service:service_provider_detail', kwargs={'pk': service_provider.id}))
