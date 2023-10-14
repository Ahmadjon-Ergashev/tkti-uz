from rest_framework import serializers

from main.models.posts import StudyProgram

class StudyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyProgram
        fields = "__all__"

