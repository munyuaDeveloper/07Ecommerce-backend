from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from django.contrib.auth.models import User,Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from users.models import CustomUser
User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    user_type = serializers.CharField(allow_null=True,allow_blank=True)
    name = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user_type = validated_data['user_type']
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        if user_type:
            # fetch details of the group selected
            try:
                group_instance = Group.objects.get(name=user_type)
            except Exception as e:
                raise serializers.ValidationError("Group does not exist")
            user.groups.add(group_instance)

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token
class GroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name =  serializers.CharField()
class UserSerializer(serializers.ModelSerializer):
    user_roles = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name','user_roles']
    def get_user_roles(self,obj):
        all_roles =  obj.groups.all()
        records = GroupSerializer(all_roles,many=True)
        return records.data
