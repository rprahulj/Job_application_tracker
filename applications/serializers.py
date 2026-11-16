from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Application, Interview, Note, Reminder

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = "__all__"
        read_only_fields = ("created_at",)
    def validate_application(self, value):
        request = self.context["request"]
        if value.user_id != request.user.id:
            raise serializers.ValidationError("Application does not belong to you.")
        return value

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
    def validate_application(self, value):
        if value.user_id != self.context["request"].user.id:
            raise serializers.ValidationError("Application does not belong to you.")
        return value

class ReminderSerializer(serializers.ModelSerializer):
    is_sent = serializers.BooleanField(read_only=True)
    class Meta:
        model = Reminder
        fields = "__all__"
        read_only_fields = ("sent_at", "created_at")
    def validate_application(self, value):
        if value.user_id != self.context["request"].user.id:
            raise serializers.ValidationError("Application does not belong to you.")
        return value
