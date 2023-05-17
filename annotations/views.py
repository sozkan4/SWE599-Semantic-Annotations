from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Movie, Annotation
from .forms import AnnotationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm

class CustomUserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'templates/registration/register.html'
    success_url = reverse_lazy('annotations:movies')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object) 
        return valid

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('annotations:movies')
        return super().get(request, *args, **kwargs)

@login_required
def profile(request):
    return render(request, 'registration/profile.html')
    
class MovieListView(ListView):
    model = Movie
    template_name = 'annotations/movies.html'

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'annotations/movie_detail.html'

@method_decorator(login_required, name='dispatch')
class AnnotationCreateView(CreateView):
    model = Annotation
    form_class = AnnotationForm
    template_name = 'annotations/annotation_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = self.kwargs['movie_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('annotations:movie_detail', args=[str(self.kwargs['movie_id'])])
