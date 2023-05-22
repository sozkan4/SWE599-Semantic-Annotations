from django.urls import path
from .views import AnnotationList, AnnotationDetail, AnnotationSearch

urlpatterns = [
    path('', AnnotationList.as_view(), name='annotation-list'),
    path('<int:pk>/', AnnotationDetail.as_view(), name='annotation-detail'),
    path('search/', AnnotationSearch.as_view(), name='annotation-search'),
]
