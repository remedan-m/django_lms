from rest_framework import serializers
from members.models import Member
from django.contrib.auth.password_validation import validate_password


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class MemberRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        field = '__all__'
        exclude = ['start_date', 'is_staff', 'is_superuser']
        
    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('Passwords do not match.')
        
        return data
    
    def create(self, valid_data):
        member = Member.objects.create_user(
            email = valid_data['email'],
            username = valid_data['username'],
            first_name = valid_data['first_name'],
            contact = valid_data['contact'],
            address = valid_data['address'],
            about = valid_data['about'],
            # is_staff = valid_data['is_staff'],
            is_active = valid_data['is_active'],

        )

        return member
    

class AdminRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        field = '__all__'
        exclude = ['start_date']
        
    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('Passwords do not match.')
        
        return data
    
    def create(self, valid_data):
        admin = Member.objects.create_user(
            email = valid_data['email'],
            username = valid_data['username'],
            first_name = valid_data['first_name'],
            contact = valid_data['contact'],
            address = valid_data['address'],
            about = valid_data['about'],
            is_staff = valid_data['is_staff'],
            is_active = valid_data['is_active'],

        )

        return admin
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password= serializers.CharField(required=True)
    new_password= serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError('old password is nor correct.')
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
