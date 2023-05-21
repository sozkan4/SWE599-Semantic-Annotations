from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Annotation
from .serializers import AnnotationSerializer

class AnnotationCreate(APIView):
    """
    Handles requests to create a new annotation.

    POST: Creates a new annotation based on the data included in the request.
    """

    def post(self, request, format=None):
        # Create a new annotation based on the request data
        serializer = AnnotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnotationList(APIView):
    """
    Handles requests to the root endpoint ("/").

    GET: Returns a list of all annotations in the database.
    POST: Creates a new annotation based on the data included in the request.
    """

    def get(self, request, format=None):
        # Retrieves all annotations from the database.
        annotations = Annotation.objects.all()
        # Converts the annotations to JSON using the serializer.
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Creates a new annotation based on the request data.
        serializer = AnnotationSerializer(data=request.data)
        if serializer.is_valid():
            # Saves the annotation to the database.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnotationDetail(APIView):
    """
    Handles requests to the annotation detail endpoint ("/<annotation_id>").

    GET: Returns the details of the specified annotation.
    PUT: Updates the specified annotation based on the data included in the request.
    DELETE: Deletes the specified annotation.
    """

    def get_object(self, annotation_id):
        # Retrieves the annotation with the given annotation_id from the database.
        try:
            return Annotation.objects.get(annotation_id=annotation_id)
        except Annotation.DoesNotExist:
            # Raises a 404 error if the annotation is not found.
            raise Http404

    def get(self, request, annotation_id, format=None):
        # Retrieves the annotation and converts it to JSON.
        annotation = self.get_object(annotation_id)
        serializer = AnnotationSerializer(annotation)
        return Response(serializer.data)

    def put(self, request, annotation_id, format=None):
        # Updates the annotation based on the request data.
        annotation = self.get_object(annotation_id)
        serializer = AnnotationSerializer(annotation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, annotation_id, format=None):
        # Deletes the annotation.
        annotation = self.get_object(annotation_id)
        annotation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnnotationSearch(APIView):
    """
    Handles requests to the annotation search endpoint ("/search/?query=<query>").

    GET: Returns a list of annotations that match the search query.
    """

    def get(self, request):
        # Retrieves the search query from the request.
        query = request.GET.get("query", "").strip()
        if not query:
            # Returns an error if the query parameter is missing.
            return JsonResponse({"error": "Missing query parameter"}, status=400)

        # Retrieves annotations that match the search query.
        annotations = Annotation.objects.filter(Q(body__icontains=query))
        # Converts the annotations to JSON.
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)

