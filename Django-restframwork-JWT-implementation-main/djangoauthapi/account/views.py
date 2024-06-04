from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views, parsers
from rest_framework.views import APIView
from account.serializers import *
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



# Create your views here.
#generating Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    # renderer_classes =[UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'message':'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
    

class UserLoginView(APIView):
    # renderer_classes =[UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password= serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'Message':'Login success'}, status=status.HTTP_200_OK)
            else:
                return Response({'non_field_errors':['Email or Password is not Valid']},status=status.HTTP_404_NOT_FOUND)


        return Response({})
    
class FileUploadView(APIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, format=None):
        file_obj = request.FILES['file']  # 'file' is the name of the key in the form-data
        # Save the file
        file_name = default_storage.save(file_obj.name, file_obj)
        file_url = default_storage.url(file_name)

        return Response({'url': file_url, 'message': 'File uploaded successfully!'}, status=status.HTTP_201_CREATED)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer =  UserProfileSerializer(request.user)
        # if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'Password Updated'},status=status.HTTP_200_OK )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
    