from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_expiring_authtoken import authentication

from api.serializers import UserSerializer, SnippetSerializer


class UserList(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetList(APIView):
    authentication_classes = (authentication.ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
