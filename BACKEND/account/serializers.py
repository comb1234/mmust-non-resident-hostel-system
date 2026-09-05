from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role',
                  'registration_number', 'phone', 'gender', 'course', 'year_of_study']
        read_only_fields = ['id', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name',
                  'registration_number', 'phone', 'gender', 'course', 'year_of_study']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}, 'email': {'required': True}}

    def validate_email(self, value):
        if not value.endswith('@student.mmust.ac.ke'):
            raise serializers.ValidationError("Email must be a valid MMUST student email.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            registration_number=validated_data.get('registration_number', ''),
            phone=validated_data.get('phone', ''),
            gender=validated_data.get('gender', ''),
            course=validated_data.get('course', ''),
            year_of_study=validated_data.get('year_of_study', None),
        )
        user.role = 'student'
        user.save()
        return user