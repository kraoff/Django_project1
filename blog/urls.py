from django.urls import path
from .views import registration,redirect_to_user_profile,login_in,PostSearchResultsView, get_post_by_title
from .views import BlogListView, AboutPageView, ImputPageView, UserProfileView
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import ListView
from django.urls import reverse_lazy


    

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('imput/', ImputPageView.as_view(), name='imput'),
    path('register/', registration, name='register'),
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('registration_success/', redirect_to_user_profile, name='registration_success'),
    path('login/', LoginView.as_view(template_name='home.html', redirect_authenticated_user=True, success_url=reverse_lazy('home')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', PostSearchResultsView.as_view(), name='search_results'),
    path('<str:title>/', get_post_by_title )# Маршрут для обработки поиска

]
