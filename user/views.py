from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import status, generics, renderers
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action, renderer_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser

from rest_framework.authtoken.models import Token

from . import custompermissions, custompagination
from .models import User, Role, UserRole, Family, Profile
from .serializers import UserRegistrationSerializer, UserRoleSerializer, UserLoginSerializer, UserProfileSerializer, \
    ProfileSerializer, UserFamilyListSerializer


# @api_view(['POST', ])
# def user_register(request):
#     data = {}
#     if request.method == 'POST':
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = 'successfully registered'
#             data['email'] = user.email
#             data['phone_number'] = user.phone_number
#         else:
#             data = serializer.errors
#         return Response(data)


class Register(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    pagination_class = custompagination.CustomPagination
    filter_fields = ['email', 'first_name', 'last_name']
    search_fields = ('email', 'first_name', 'last_name')

    def post(self, request, format=None, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def user_login(request):
    print(request.user)
    data = {}
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = Token.objects.get(user__email=email)
            data['email'] = email
            data['token'] = token.key
            return Response(data)
        return Response(serializer.errors)


# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def users_role(request):
#     if request.method == "GET":
#         user = request.user
#         users_role = User.objects.filter(family=user)
#         serializer = UserRoleSerializer(users_role, many=True)
#         return Response(serializer.data)
#     else:
#         serializer = UserRoleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes([TokenAuthentication])
@permission_classes([custompermissions.IsCurrentUserOwner])
@renderer_classes([JSONRenderer])
def user_family_member_list(request):
    data = {}
    user = request.user
    family_member_list = User.objects.filter(family=user.family).exclude(email=user.email)
    serializer = UserFamilyListSerializer(family_member_list, many=True)
    return Response(serializer.data)


# class UserProfile(APIView):
#
#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(User, pk=kwargs['pk'])
#         profile_serializer = UserProfileSerializer(user.profile)
#         return Response(profile_serializer.data)


class UserProfile(ModelViewSet):
    serializer_class = UserProfileSerializer
    # permission_classes = [custompermissions.IsOwnerUser]
    queryset = User.objects.all()
    lookup_field = 'pk'

    # def get_queryset(self):
    #     obj = Profile.objects.filter(user=self.request.user)
    #     print(obj)
    #     return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserProfileSerializer(instance=instance, data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(serializer.data)
        return Response(serializer.data)

    # @action(detail=True, url_path='update_profile', methods=['put'])
    # def profile(self, request, pk=None):
    #     user = self.get_object()
    #     profile = user.profile
    #     serializer = ProfileSerializer(profile, data=request.data)
    #     parser_classes = (JSONParser, FormParser, MultiPartParser)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoleApiView(APIView):
    serializer_class = UserRoleSerializer
    permission_classes = [custompermissions.IsCurrentUserOwner]

    def get_queryset(self):
        users_role_for_user = UserRole.objects.filter(user1__pk=self.request.user.pk)
        return users_role_for_user

    def get(self, request, format=None):
        querset = self.get_queryset()
        serializer = UserRoleSerializer(querset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user1=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, format=None):
    #     instanse =  UserRole.objects.filter(user1=request.data['user1'], user2=request.data['user2'])
    #     serializer = UserRoleSerializer(instanse=instanse, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #


class FamilyMembersListView(generics.ListAPIView):
    serializer_class = UserFamilyListSerializer
    permission_classes = (custompermissions.IsCurrentUserOwner,)
    pagination_class = custompagination.CustomPagination

    def get_queryset(self):
        queryset = User.objects.filter(family=self.request.user.family).exclude(email=self.request.user.email)
        return queryset
