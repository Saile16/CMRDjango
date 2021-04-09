from django.core.mail import send_mail

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
# Create your views here.
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm


class SignupView(generic.CreateView):
    # cuando usamos classviews estos pasan un "contexto" automatico
    # lleva por nombre object_list
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


#CRUD -Create,Retrievce,Update and DELETE + list
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, generic.ListView):
    # cuando usamos classviews estos pasan un "contexto" automatico
    # lleva por nombre object_list
    template_name = "leads/lead_list.html"
    # sin embargo podemos cambiar a lo que deseemos
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, agent__isnull=False)
            # filtrar por el agente que esta logeado
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


def lead_list(request):
    # return HttpResponse("Hello World")
    # return render(request, "leads/home_page.html")
    leads = Lead.objects.all()
    context = {
        "leads": leads,
    }
    return render(request, "leads/lead_list.html", context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    # en este caso incluso no tenemos que llamar a la primary key django lo hace
    # por nosotros
    # cuando usamos classviews estos pasan un "contexto" automatico
    # lleva por nombre object_list
    template_name = "leads/lead_detail.html"
    # sin embargo podemos cambiar a lo que deseemos
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            # filtrar por el agente que esta logeado
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    print(lead)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    # cuando usamos classviews estos pasan un "contexto" automatico
    # lleva por nombre object_list
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # TODo SEND EMAIL
        # estamos probando enviar email stos son los valores por defecto que viene
        # en la documentacion leer mas
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        # print("Receiving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
    }
    return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        # print("Receiving a post request")
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }

    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             print("The lead has been created")
#             return redirect("/leads")
#     context = {
#         "form": form,
#         "lead": lead
#     }
#     return render(request, "leads/lead_update.html", context)

# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         print("Receiving a post request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent,
#             )
#             print("The lead has been created")
#             return redirect("/leads")
#     context = {
#         "form": form,
#     }
#     return render(request, "leads/lead_create.html", context)
