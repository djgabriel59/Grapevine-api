from rest_framework import serializers
from .models import Project, Skill, User, CollaborationRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "age", "country", "residence", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}, "username": {"read_only": True}}


    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save(update_fields=['password'])
        print(instance)
        return instance

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "language", "level", "user"]
        extra_kwargs = {"user": {"read_only": True}}

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

   
class CollaborationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model: CollaborationRequest
        fields = "__all__"

class UserStatisticsSerializer(serializers.Serializer):
    projects_created = serializers.IntegerField()
    projects_contributed = serializers.IntegerField()
