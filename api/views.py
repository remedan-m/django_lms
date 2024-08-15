from members.models import Member
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, get_connection
from django.urls import reverse


# Create your views here.

'''class RoutesView(APIView):
    def get(self, request, *args, **kwargs):
        routes = [
        {
            'Endpoint:': '/members/register/',
            'method': 'Post',
            'title': None,
            'description': 'signup endpoint for members'
        },

        {
            'Endpoint:': '/members/admin/register/',
            'method': 'Post',
            'title': None,
            'description': 'signup endpoint for only admin members'
        },

        {
            'Endpoint:': '/logout/',
            'method': 'POST',
            'title': None,
            'description': 'login out endpoint'
        },

                {
            'Endpoint:': '/token/',
            'method': 'Post',
            'title': None,
            'description': 'endpoint to issue token refresh'
        },

        {
            'Endpoint:': '/token/refresh/',
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

        {
            'Endpoint:': '/password-change/',
            'method': 'PUT/PATCH',
            'title': None,
            'description': 'updates the password for the authenticated user(member)'
        },
    ]
        
        return Response(routes)'''


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


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Member
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': 'wrong_password'}, status=400)
            
            user.set_password(serializer.data.get('new_password'))
            user.save()

            return Response({'details': 'Password updated successfully.'})
        
        return Response(serializer.errors, status=400)
            

class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = Member.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{request.scheme}://{request.get_host()}/password-reset-confirm/{uid}/{token}/"

        #connection = get_connection('django.core.mail.backends.console.EmailBackend')

        send_mail(
            'Password Reset Request',
            f'Here is your password reset link: {reset_link}',
            'from@example.com',
            [email],
            fail_silently=False,
            #connection=connection
            
        )
        return Response({"detail": "Password reset link sent."})


class PasswordResetConfirmView(generics.UpdateAPIView):
    serializer_class = SetNewPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'uidb64': kwargs['uidb64'], 'token': kwargs['token']})
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Password reset successfully."})