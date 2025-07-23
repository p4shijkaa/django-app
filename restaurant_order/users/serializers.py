from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ['name']


class UserSerializer(serializers.ModelSerializer):
	groups = GroupSerializer(many=True, read_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name',
				  'user_type', 'phone', 'groups', 'is_staff']
		read_only_fields = ['is_staff']


class StaffUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'user_type', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'phone', 'first_name', 'last_name']

	def create(self, validated_data):
		user = User.objects.create_user(
			username=validated_data['username'],
			password=validated_data['password'],
			email=validated_data.get('email', ''),
			phone=validated_data.get('phone', ''),
			first_name=validated_data.get('first_name', ''),
			last_name=validated_data.get('last_name', '')
		)
		return user
