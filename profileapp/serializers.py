from .models import UserProfile,ChageProfile
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response

class ProfileSerilizer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile','profile_picture','address','bio']

    def check_user(self,request):
        if UserProfile.objects.filter(profile=request.user):
            return Response({'message':"user profile is already existed"})    
        

class ChageProfileSerilizer(ModelSerializer):
    class Meta:
        model = ChageProfile
        fields = '__all__'     