from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'annotations'

urlpatterns = [
    path('', views.CustomUserCreateView.as_view(), name='register'),
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('movies/<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:movie_id>/annotate/', views.AnnotationCreateView.as_view(), name='add_annotation'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
]

