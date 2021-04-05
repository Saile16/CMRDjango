from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import Lead, Agent
from .forms import LeadForm


def lead_list(request):
    # return HttpResponse("Hello World")
    # return render(request, "leads/home_page.html")
    leads = Lead.objects.all()
    context = {
        "leads": leads,
    }
    return render(request, "leads/lead_list.html", context)


def lead_detail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    print(lead)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)


def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        print("Receiving a post request")
        form = LeadForm(request.POST)
        if form.is_valid():
            print("form is valid")
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.first()
            Lead.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                agent=agent,
            )
            print("The lead has been created")
            return redirect("/leads")
    context = {
        "form": form,
    }
    return render(request, "leads/lead_create.html", context)