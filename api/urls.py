from django.urls import path, include
from . import views
from .views import MemberList, MemberDetail, MemberRegisterView, AdminRegisterView, LogoutView
from members.models import Member
from .serializers import MemberSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('members/register/', MemberRegisterView.as_view(), name='register'),
    path('members/admin/register/', AdminRegisterView.as_view(), name='admin_register'),
    
    path('members/logout/', LogoutView.as_view(), name='logout'),
    # path('members/', include('rest_framework.urls')),

    path('members/', MemberList.as_view(), name='members'),
    path('members/<int:pk>/', MemberDetail.as_view(queryset=Member.objects.all(), serializer_class=MemberSerializer), name='member'),
]
