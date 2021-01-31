from rest_framework import serializers
from .models import Chapter, Concept


class ConceptCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

    description = serializers.CharField()


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = ['name', 'subject', 'description']


class ChapterCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    subject = serializers.CharField()
    description = serializers.CharField()
    concept = ConceptCreateSerializer(many=True,  help_text="[ { \"name\": \"name\",  \"description\": \"description\" }]")

    class Meta:
        model = Chapter
        fields = ['name', 'subject', 'description' ,  'concept']

    def create(self, *args, **kwargs):
        data = self.validated_data.pop('concept')
        chapter = Chapter.objects.create(
            name=self.validated_data['name'],
            subject=self.validated_data['subject'],
            description=self.validated_data['description'],
        )

        for concept in data:
            Concept.objects.create(
                name=concept['name'],
                description=concept['description'],
                chapter=chapter
            )
        return chapter


class ConceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concept
        fields = ['name',  'description', 'chapter']