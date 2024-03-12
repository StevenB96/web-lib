from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)