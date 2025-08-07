from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import UserProfile,User,ChageProfile
from rest_framework.views import APIView
from .serializers import ProfileSerilizer,ChageProfileSerilizer
from rest_framework import permissions




class uplaod_profile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        serializer = ProfileSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=request.user)
            return Response({'message':'profile successfully uploaded','status':'success'},
                            status=status.HTTP_201_CREATED)
        return Response({'message':'profile already exited','status':'failed'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    


class update_profile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        user_id = request.data.get('user_id')
        try:
            profile_id = UserProfile.objects.get(id=user_id)
            print(request.user.first_name)
            print(request.user.id)
            print(profile_id.id)
            if profile_id.profile != request.user:
                 return Response({'message':'you are not allowed to update this profile'})
            serialisers = ProfileSerilizer(profile_id,data=request.data,partial=True)
            if serialisers.is_valid():
               serialiser = serialisers.save()
               ChageProfile.objects.create(profile=profile_id,new_photo=serialiser.profile_picture)
               return Response({'message':'profile succesfully update','status':'success'},
                                 status=status.HTTP_201_CREATED)
            return Response({'message':'profile failed to update','status':'failed'},
                                    status=status.HTTP_400_BAD_REQUEST)
                
        
        except UserProfile.DoesNotExist:
                   return Response({'id not found'})
        