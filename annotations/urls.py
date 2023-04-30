from django.urls import path
from . import views

app_name = 'annotations'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/annotate/', views.AnnotationCreateView.as_view(), name='annotation_create'),
]
