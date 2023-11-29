from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


from main.models import posts


class StudyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts.StudyProgram
        fields = "__all__"


class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = posts.Posts
        fields = "__all__"


class ShortPostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = posts.Posts
        fields = ["id", "title"]


class FacultySerializers(serializers.ModelSerializer):
    class Meta:
        model = posts.Posts
        fields = ["id", "title", "slug"]
        

class DepartmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = posts.Departments
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["faculty"] = FacultySerializers(instance=instance.faculty).data
        return data
    

class AdmistationSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts.UniversityAdmistrations
        fields = [
            "id", "image", "f_name", "position", "email", "phone",
            "admission_days", "short_info", "scientific_direction",
            "main_tasks_in_position", "scientific_activity", "facebook", "instagram", "linkedin"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["short_info"] = instance.short_info.html
        data["scientific_direction"] = instance.scientific_direction.html
        data["main_tasks_in_position"] = instance.main_tasks_in_position.html
        data["scientific_activity"] = instance.scientific_activity.html
        data["read_more"] = _("Batafsil")
        data["short_info_title"] = _("Qisqacha ma'lumot")
        data["scientific_direction_title"] = _("Ilmiy yo'nalishlari")
        data["main_tasks_in_position_title"] = _("Lavozimidagi asosiy vazifalar")
        data["scientific_activity_title"] = _("Ilmiy va pedagogik mehnat faoliyati")
        return data
    

class TalentedStudentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = posts.TalentedStudents
        fields = '__all__'


class StudyDegreesSerialziers(serializers.ModelSerializer):
    faculty = FacultySerializers(many=True)
    class Meta:
        model = posts.StudyDegrees
        fields = ["id", "name", "faculty"]
    

class LearningWaySerializers(serializers.ModelSerializer):
    class Meta:
        model = posts.LearningWay
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["study_degree"] = StudyDegreesSerialziers(instance=instance.study_degree).data
        data["faculty"] = ShortPostsSerializers(instance=instance.faculty).data
        return data



    