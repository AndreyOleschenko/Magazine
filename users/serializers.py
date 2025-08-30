from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='Имя пользователя')
    email = serializers.EmailField(label='Электронная почта')
    password = serializers.CharField(write_only=True, label='Пароль')
    user_type = serializers.ChoiceField(
        choices=[('consumer', 'Потребитель'), ('supplier', 'Поставщик')],
        label='Тип пользователя'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value
            
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован")
        return value
       
    def create(self, validated_data):
        user =  User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
            )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='Имя пользователя')
    email = serializers.EmailField(label='Электронная почта')
    user_type = serializers.ChoiceField(
        choices=[('consumer', 'Потребитель'), ('supplier', 'Поставщик')],
        label='Тип пользователя'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True}
        }