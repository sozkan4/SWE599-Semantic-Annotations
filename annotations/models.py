from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
        
class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assumes you're using Django's built-in User model for authentication
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    annotation_type = models.CharField(max_length=255)  # E.g., 'text', 'image', etc.
    target = models.TextField()  # Reference to the annotated text or image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
