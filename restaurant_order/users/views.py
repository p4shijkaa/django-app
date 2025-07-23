from rest_framework import generics, permissions

from .models import User
from .serializers import UserSerializer, RegisterSerializer, StaffUserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user


class RegisterView(generics.CreateAPIView):
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]


class StaffUserListView(generics.ListAPIView):
	permission_classes = [permissions.IsAdminUser]
	serializer_class = StaffUserSerializer
	queryset = User.objects.filter(is_staff=True)
