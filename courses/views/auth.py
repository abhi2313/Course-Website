from django.shortcuts import render, HttpResponse, redirect
from courses.forms import RegistrationForm, loginForm
from django.views import View
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView


class signUpView(FormView):
    template_name = "courses/signup.html"
    form_class = RegistrationForm
    success_url = '/login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


'''
class signUpView(View):
    def get(self, request):
        if request.method == 'GET':
            form = RegistrationForm()
            return render(request, template_name="courses/signup.html", context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                return redirect('login')

        return render(request, template_name="courses/signup.html", context={'form': form})
'''
# instead of this class bases view i can use formview for handling forms.


class LoginView(View):

    def get(self, request):
        if request.method == 'GET':
            form = loginForm()
            context = {
                "form": form
            }
            return render(request, template_name="courses/login.html", context=context)

    def post(self, request):
        form = loginForm(request=request, data=request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            return redirect('home')

        return render(request, template_name="courses/login.html", context=context)


def signOut(request):
    logout(request)
    return redirect('home')
