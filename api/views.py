from members.models import Member
from .serializers import MemberSerializer, MemberRegisterSerializer, AdminRegisterSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from members.models import Member



# Create your views here.

@api_view(['GET'])
def getRoutes(request):
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
            'Endpoint:': 'members/login/',
            'method': 'Post',
            'title': None,
            'description': 'login endpoint'
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

    

class MemberList(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]


class MemberDetail(generics.RetrieveDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]


