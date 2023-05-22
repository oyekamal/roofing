from django.shortcuts import render
from .forms import ServiceRequestForm

# Create your views here.
def home(request):

    return render(request, "service/home.html")


def service_request(request):
    if request.method == "GET":
        form = ServiceRequestForm
        mydict = {
            "form": form,
        }
        return render(request, "service/service-request.html", context=mydict)
    else:
        try:
            request.POST._mutable = True
            request_data = request.POST.copy()
            print(request.user)
            print(request.user.id)
            print(request)
            request_data["client"] = request.user.id
            request_data["status"] = "Open"
            form = ServiceRequestForm(request_data)
            if form.is_valid():
                form.save()
                return render(
                    request, "service/service-request.html", {"form": form, "success": True}
                )
            else:
                print(form.errors)
        except Exception as e:
            print(e)
        return render(request, "service/service-request.html", {"form": form})