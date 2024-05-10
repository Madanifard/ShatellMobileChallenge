from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'user/login.html'

class RegisterView(TemplateView):
    template_name = 'user/register.html'

class UserInfoView(TemplateView):
    template_name = 'user/user_info.html'