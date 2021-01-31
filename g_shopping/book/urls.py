from django.urls import path, re_path, include
from rest_framework import routers
from .api import ConceptView, ChapterView

router = routers.DefaultRouter()
router.register('concept', ConceptView, 'concept')
router.register('chapter', ChapterView, 'chapter')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]