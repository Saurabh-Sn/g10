from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Concept, Chapter
from .serializers import ChapterSerializer, ConceptSerializer, ChapterCreateSerializer


class ChapterView(mixins.ListModelMixin,  mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer = ChapterSerializer
        if self.action == 'create':
            serializer = ChapterCreateSerializer
        return serializer

    def create(self, request, *args, **kwargs):
        serialized = ChapterCreateSerializer(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            chapter = serialized.create()
            serialized = ChapterSerializer(chapter)
            return Response(serialized.data, status=201)
        raise Http404


class ConceptView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ConceptSerializer
    queryset = Concept.objects.all()
    permission_classes = [IsAuthenticated]
