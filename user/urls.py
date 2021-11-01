from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.UserProfile, 'profile')


urlpatterns = [
    path('djoser/', include('djoser.urls')),
    path('djoser/', include('djoser.urls.authtoken')),
    path('login', views.user_login, name='login'),
    # path('users_roles/', views.users_role, name='users_role'),
    path('users_family_member_list/', views.FamilyMembersListView.as_view(), name='users_family_member_list'),
    # path('users_family_member_list/', views.user_family_member_list, name='users_family_member_list'),
    path('register/', views.Register.as_view(), name='register'),
    path('profile/', include(router.urls)),
    path('users_role/', views.UserRoleApiView.as_view(), name='users_role'),
    path('', views.APIView.as_view())
]
