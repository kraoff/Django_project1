from django.views.generic import ListView, TemplateView
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .forms import WriterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import View
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import Post
from django.views.generic import DetailView
import pickle



class PostSearchResultsView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        object_list = Post.objects.filter(title__icontains=query)
        return render(request, self.template_name, {'object_list': object_list, 'query': query})


def get_post_by_title(request, title):
    post = get_object_or_404(Post, title=title)
    user_authenticated = request.user.is_authenticated
    return render(request, 'post_detail.html', {'post': post,'user_authenticated':user_authenticated  })





class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})



def redirect_to_user_profile(request):
    return redirect('user_profile')

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Profile
from django.views.generic import UpdateView

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = '/user_profile/'  # Укажите URL, куда перейти после успешного обновления профиля

    def get_object(self, queryset=None):
        return self.request.user.profile




def registration(request):
    print(request.method)
    if request.method =='POST':
        form = WriterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html')
    else:
        form = UserCreationForm()
    return render(request, 'your_template.html', {'form': form})


def login_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_authenticated'] = True
            return render(request, 'home.html')
            # return redirect('profile')
    
    return render(request, 'home.html', {'object_list': Post.objects.all()})




class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    paginate_by = 3
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WriterForm()
        context['login_form'] = CustomAuthenticationForm()
        context['user_authenticated'] = self.request.user.is_authenticated
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_authenticated'] = self.request.user.is_authenticated
        return context


class ImputPageView(TemplateView):
    template_name = 'imput.html'


from django.shortcuts import render
import pickle


def home(request):
    return render(request, 'Input.html')


def getPredictions(pclass, sex, age, sibsp, parch, fare, C, Q, S):
    model = pickle.load(open('ml_model.sav', 'rb'))
    scaled = pickle.load(open('scaler.sav', 'rb'))

    prediction = model.predict(scaled.transform([
        [pclass, sex, age, sibsp, parch, fare, C, Q, S]
    ]))

    if prediction == 0:
        return 'no'
    elif prediction == 1:
        return 'yes'
    else:
        return 'error'


def result(request):
    pclass = int(request.GET['pclass'])
    sex = int(request.GET['sex'])
    age = int(request.GET['age'])
    sibsp = int(request.GET['sibsp'])
    parch = int(request.GET['parch'])
    fare = int(request.GET['fare'])
    embC = int(request.GET['embC'])
    embQ = int(request.GET['embQ'])
    embS = int(request.GET['embS'])

    result = getPredictions(pclass, sex, age, sibsp,
                            parch, fare, embC, embQ, embS)

    return render(request, 'Result.html', {'result': result})