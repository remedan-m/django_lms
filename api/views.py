from members.models import Member
from .serializers import MemberSerializer, MemberRegisterSerializer, AdminRegisterSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from members.models import Member

# Create your views here.

class RoutesView(APIView):
    def get(self, request, *args, **kwargs):
        routes = [
        {
            'Endpoint:': 'members/register/',
            'method': 'Post',
            'title': None,
            'description': 'signup endpoint for members'
        },

        {
            'Endpoint:': 'members/admin/register/',
            'method': 'Post',
            'title': None,
            'description': 'signup endpoint for only admin members'
        },

        {
            'Endpoint:': 'members/logout/',
            'method': 'POST',
            'title': None,
            'description': 'login out endpoint'
        },

                {
            'Endpoint:': 'token/refresh/',
            'method': 'Post',
            'title': None,
            'description': 'endpoint to issue token refresh'
        },

        {
            'Endpoint:': 'token/',
            'method': 'Post',
            'title': None,
            'description': 'endpoint to issue a token'
        },

        {
            'Endpoint:': '/members/',
            'method': 'GET',
            'title': None,
            'description': 'reterns an array of registered members'
        },

        {
            'Endpoint:': '/members/id',
            'method': 'GET',
            'title': None,
            'description': 'reterns details of registered member'
        },
    ]
        
        return Response(routes)


class MemberRegisterView(generics.CreateAPIView):
    serializer_class = MemberRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data,
        status=status.HTTP_201_CREATED, headers=headers
        )


class AdminRegisterView(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
        serializer.data,
        status=status.HTTP_201_CREATED, headers=headers
        )


class LogoutView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidate the refresh token

            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
   

class MemberList(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]


class MemberDetail(generics.RetrieveDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]


