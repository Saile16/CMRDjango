from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganisorAndLoginRequiredMixin(AccessMixin):
    # esta clase la creamos para que solo los usuarios con permisor de organizdor puedan ver las funciones
    # permitidas es una funcionalidad nuestra
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("leads:lead-list")
        return super().dispatch(request, *args, **kwargs)
