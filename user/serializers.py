from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Role, UserRole, Family, Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'family', 'role', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            family=self.validated_data['family'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.save()
        profile = Profile.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get('email'))
        if not user.exists():
            raise serializers.ValidationError({'email': ['There is no such user in our server']})
        user = user.first()
        password = attrs.get('password')
        if not user.check_password(password):
            raise serializers.ValidationError({'password': ['Incorrect password']})
        return attrs


class UserRoleSerializer(serializers.ModelSerializer):
    user1 = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    user2 = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name')

    class Meta:
        model = UserRole
        fields = ('id', 'user1', 'user2', 'role')

    def validate(self, attrs):
        user1 = attrs.get('user1')
        user2 = attrs.get('user2')
        try:
            users_role = UserRole.objects.filter(user1__email=user1.email, user2__email=user2.email)
        except UserRole.DoesNotExist:
            return attrs
        if users_role:
            raise serializers.ValidationError(f'user {user2} has already had a role')
        else:
            return attrs


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, )

    class Meta:
        model = Profile
        fields = ('image',)

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name',
                  'family', 'role', 'is_superuser', 'is_staff', 'profile')

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        pk = self.context['pk']
        user_profile = Profile.objects.get(pk=pk)
        user_profile.user = instance
        user_profile.image = profile['image']
        user_profile.save()
        return super(UserProfileSerializer, self).update(instance, validated_data)


class UserFamilyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')