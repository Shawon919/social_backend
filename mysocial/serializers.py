from rest_framework.serializers import ModelSerializer

from .models import User


class UserRegistration(ModelSerializer):
    

    class Meta:
        model = User
        fields = ["first_name", "last_name", "photo", "email", "mobile_no", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
       
    
        


class UserView(ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }




class UserSerilizer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name']