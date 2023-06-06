from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Annotation
from .serializers import AnnotationSerializer


@csrf_exempt
def create_annotation(request):
    if request.method == 'POST':
        serializer = AnnotationSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def update_annotation(request, annotation_id):
    try:
        annotation = Annotation.objects.get(pk=annotation_id)
    except Annotation.DoesNotExist:
        return JsonResponse({"error": "Annotation does not exist"}, status=404)

    if request.method == 'PUT':
        serializer = AnnotationSerializer(annotation, data=request.PUT)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def delete_annotation(request, annotation_id):
    try:
        annotation = Annotation.objects.get(pk=annotation_id)
    except Annotation.DoesNotExist:
        return JsonResponse({"error": "Annotation does not exist"}, status=404)

    if request.method == 'DELETE':
        annotation.delete()
        return JsonResponse({}, status=204)


class AnnotationList(APIView):
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


class AnnotationDetail(APIView):
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


class AnnotationSearch(APIView):
    def get(self, request):
        query = request.GET.get("query", "").strip()
        if not query:
            return JsonResponse({"error": "Missing query parameter"}, status=400)

        annotations = Annotation.objects.filter(Q(body__icontains=query))
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)
