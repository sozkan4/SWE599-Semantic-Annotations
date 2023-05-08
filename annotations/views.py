from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Movie, Annotation
from .forms import AnnotationForm

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
