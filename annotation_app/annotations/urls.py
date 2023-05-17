from django.urls import path, re_path

from .views import AnnotationDetail, AnnotationList, AnnotationSearch

urlpatterns = [
    path("", AnnotationList.as_view(), name="annotations"),
    path("search/", AnnotationSearch.as_view(), name="annotation_search"),
    re_path(r"^(?P<annotation_id>[\w:/.#?!\-]+)/$", AnnotationDetail.as_view(), name="annotation_detail"),
]
