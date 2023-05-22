from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Annotation
from .serializers import AnnotationSerializer


# http://127.0.0.1:81/
class AnnotationList(APIView):
    """
    List all annotations, or create a new annotation.
    """

    def get(self, request, format=None):
        annotations = Annotation.objects.all()
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AnnotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# http://127.0.0.1:81/<id> : http://example.org/anno2
class AnnotationDetail(APIView):
    """
    Retrieve, update or delete a annotation instance.
    """

    def get_object(self, pk):
        try:
            return Annotation.objects.get(pk=pk)
        except Annotation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        annotation = self.get_object(pk)
        serializer = AnnotationSerializer(annotation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        annotation = self.get_object(pk)
        serializer = AnnotationSerializer(annotation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        annotation = self.get_object(pk)
        annotation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# example: http://127.0.0.1:81/search/?query=TextualBody
class AnnotationSearch(APIView):
    def get(self, request):
        query = request.GET.get("query", "").strip()
        if not query:
            return JsonResponse({"error": "Missing query parameter"}, status=400)

        annotations = Annotation.objects.filter(Q(body__icontains=query))
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)
