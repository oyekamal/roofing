from django.shortcuts import render, get_object_or_404, redirect

from .forms import ServiceRequestForm, UserProfileForm
from .models import UserProfile, ServiceRequest
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
# Create your views here.


def home(request):

    return render(request, "service/home.html")


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


def service_request(request):
    if request.method == "GET":
        form = ServiceRequestForm()

        # Check if UserProfile exists
        userprofile = UserProfile.objects.filter(user=request.user).first()
        if userprofile:
            userprofile_form = UserProfileForm(instance=userprofile)
            show_userprofile_form = False
        else:
            userprofile_form = UserProfileForm()
            show_userprofile_form = True

        mydict = {
            "form": form,
            "userprofile_form": userprofile_form,
            "show_userprofile_form": show_userprofile_form,
        }
        return render(request, "service/service_request_form.html", context=mydict)
    else:
        try:
            request.POST._mutable = True
            request_data = request.POST.copy()
            request_data["client"] = request.user.id
            request_data["status"] = "Open"
            form = ServiceRequestForm(request_data)

            # Check if UserProfile exists, if not, create it
            userprofile = UserProfile.objects.filter(user=request.user).first()
            if not userprofile:
                userprofile_data = {"user": request.user.id, "full_name": request_data.get("full_name"), "address": request_data.get(
                    "address"), "phone_number": request_data.get("phone_number"), "is_client": True}
                userprofile_form = UserProfileForm(userprofile_data)
                if userprofile_form.is_valid():
                    userprofile_form.save()

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
