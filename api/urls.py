from django.urls import path, include
from .views import *
from members.models import Member
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('', RoutesView.as_view(), name='routes'),
    path('schema/', SpectacularAPIView.as_view(), name= 'schema'),
    path('docs/', SpectacularSwaggerView.as_view(), name= 'docs'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('members/register/', MemberRegisterView.as_view(), name='register'),
    path('members/admin/register/', AdminRegisterView.as_view(), name='admin_register'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('members/', include('rest_framework.urls')),
    path('password-change/', ChangePasswordView.as_view(), name= 'password_change'),

    path('password-reset/', RequestPasswordResetView.as_view(), name= 'password_reset'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name= 'password_reset_confirm'),

    path('members/', MemberList.as_view(), name='members'),
    path('members/<int:pk>/', MemberDetail.as_view(queryset=Member.objects.all(), serializer_class=MemberSerializer), name='member'),
]
