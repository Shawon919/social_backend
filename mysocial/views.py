from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .serializers import (UserRegistration,UserView)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from .models import OTP
import random
import string
from django_celery_beat.models import CrontabSchedule,PeriodicTask
import json
from uuid import uuid4
from .tasks import send_email,delete_otp



class Registration(APIView):
    parser_classes = (MultiPartParser, FormParser)  # To accept form-data including files

    def post(self, request):
        try:
            serializer = UserRegistration(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                email = user.email
                otp = ''.join(random.choices(string.digits, k=6))
                OTP.objects.create(email=email, otp=otp)
                delete_otp.apply_async(args=[email], countdown=20)

                return Response({
                    "message": f"User registered successfully. A verification code '{otp}' has been sent to your email. Please confirm within 1 hour.",
                    "status": status.HTTP_201_CREATED,
                    "details": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "message": "Invalid user data.",
                "errors": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class otp_confirmation(APIView):
     def post(self,request):
         email = request.data.get('email')
         otp = request.data.get('otp')

         try:
             if User.objects.filter(email=email).exists():
                 email = User.objects.get(email=email)
                 otp_email = OTP.objects.get(email=email)
                 if otp_email.otp == otp:
                     otp_email.otp = ''
                     otp_email.save()
                     email.is_active = True
                     email.save()
                
                     return Response(
                         {'message':'succefully verified'},
                         status=status.HTTP_200_OK)
                 else: return Response({'message':'otp is not matched'},status=status.HTTP_401_UNAUTHORIZED)
             return Response({'message':"email doesn't exist"},status=status.HTTP_404_NOT_FOUND)     
         except Exception as e:
             return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class loginview(APIView):
    def post(self,request):
        user_email = request.data.get('user_email')
        user_password = request.data.get('user_password')

        if  user_email and user_password:
            user = authenticate(request,email = user_email,password=user_password)
            if user:
                token = RefreshToken.for_user(user)
                return Response({'user_details':{
                    'email': user_email,
                    'password':user_password,
                    'token':str(token.access_token)
                },
                'message':'success',
                'status': status.HTTP_202_ACCEPTED
                })
            else:
                return Response({"message":'email or password is invalid','status':'falid','status':'failed'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'message': 'somethis is wrong'
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)    




class get_user(APIView):
    def get(self,request):
        users = User.objects.all()
        serialisers = UserView(users,many=True)
        return Response(serialisers.data, status=status.HTTP_200_OK)
    


class forget_password(APIView):
    def post(self,request):
        email = request.data.get('email')
        
        random_numbers = string.digits
        otp = ''.join(random.choice(random_numbers) for _ in range(6))

        try:
            if OTP.objects.filter(email=email).exists():
                email = OTP.objects.get(email=email)
                email.otp = otp
                email.save()
                return Response({
                    'message' : "succesfully set the otp",
                    'status' : 'success',
                    'serializer' : {'email':email.email,
                                    'otp': email.otp
                                    }
                },status=status.HTTP_201_CREATED)
            return Response({
                'message' : 'email not found',
                'status' : 'failed'
            },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'errors' : str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
