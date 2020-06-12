from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import ProfileSerializer


class UserProfileView(APIView):
    """
    Handles api endpoints for user profile
    """

    def post(self, request):
        """
        Endpoint call for user registration
        """
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.process_create_user(request))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
