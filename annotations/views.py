from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from .models import Movie, Annotation

class MovieListView(ListView):
    model = Movie
    template_name = 'annotations/movie_list.html'

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'annotations/movie_detail.html'

@method_decorator(login_required, name='dispatch')
class AnnotationCreateView(CreateView):
    model = Annotation
    fields = ['content', 'annotation_type', 'target']
    template_name = 'annotations/annotation_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = self.kwargs['pk']
