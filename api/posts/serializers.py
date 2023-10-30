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


class FacultySerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["id", "title", "slug"]
        

class DepartmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["faculty"] = FacultySerializers(instance=instance.faculty).data
        return data