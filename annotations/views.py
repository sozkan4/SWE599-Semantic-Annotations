from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Movie, Annotation
from .forms import AnnotationForm

class MovieListView(View):
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, 'movies.html', {'movies': movies})

class MovieDetailView(View):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        annotations = Annotation.objects.filter(movie=movie)
        form = AnnotationForm()
        return render(request, 'annotations.html', {'movie': movie, 'annotations': annotations, 'form': form})

@method_decorator(login_required, name='dispatch')
class AnnotationCreateView(View):
    def post(self, request, movie_id):
        form = AnnotationForm(request.POST)
        if form.is_valid():
            annotation = form.save(commit=False)
            annotation.user = request.user
            annotation.movie_id = movie_id
            annotation.save()
            return redirect('annotations', movie_id=movie_id)
        else:
            movie = get_object_or_404(Movie, id=movie_id)
            annotations = Annotation.objects.filter(movie=movie)
            return render(request, 'annotations.html', {'movie': movie, 'annotations': annotations, 'form': form})
