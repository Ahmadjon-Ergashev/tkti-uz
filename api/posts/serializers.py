from rest_framework import serializers

from main.models.posts import (
    StudyProgram, Posts, Departments
)

class StudyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyProgram
        fields = "__all__"


class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"
        

class DepartmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = "__all__"