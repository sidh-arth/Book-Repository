from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets, status, generics, filters, serializers
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, BookSerializer, BorrowerSerializer
from .models import Book, Borrower
# Create your views here.


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if created:
            login_data = {
                'token': token.key, 'first_name': user.first_name, 
                'id': user.id, 'last_name': user.last_name, 
                'email': user.email
            }
            response_data = {
                'status_code': "200",
                'status': True,
                'message': "User logged in successfully",
                'data': login_data
            }
        else:
            response_data = {
                'status_code': "400",
                'status': False,
                'message': "User already logged in!",
                'data': {"token": token.key}
            }
                
        if response_data['status_code'] == '400':
            resp_status = status.HTTP_400_BAD_REQUEST
        elif response_data['status_code'] == '200':
            resp_status = status.HTTP_200_OK
        return Response(response_data, status=resp_status)


class UserLogout(APIView):
    permission_classes = (IsAuthenticated)

    def get(self, request, format=None):
        request.user.auth_token.delete() 
        response_data = {
            'status_code': "200",
            'status': True,
            'message': "User logged out successfully.",
        }
        return Response(response_data)


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        response_data = {
            "status_code": "200",
            "status": True,
            "message": 'Book List',
            "data": data
        }
        return Response(response_data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        response_data = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().create(request)
        if response:
            response_data['status_code'] = '201'
            response_data['status'] = True
            response_data['message'] = 'Book details entered successfully'
            response_data['data'] = serializer.data            
        else:
            response_data['status_code'] = '400'
            response_data['status'] = False
            response_data['message'] = 'Book details could not be entered'

        if response_data['status_code'] == '400':
            resp_status = status.HTTP_400_BAD_REQUEST
        elif response_data['status_code'] == '201':
            resp_status = status.HTTP_201_CREATED

        return Response(response_data, status=resp_status)


    def retireve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        response_data = {
            "status_code": "200",
            "status": True,
            "message": 'Book Details',
            "data": data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class BorrowerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        response_data = {
            "status_code": "200",
            "status": True,
            "message": 'Borrower List',
            "data": data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        response_data = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().create(request)
        
        if response:
            response_data['status_code'] = '201'
            response_data['status'] = True
            response_data['message'] = 'Book borrow details entered successfully'
        else:
            response_data['status_code'] = '400'
            response_data['status'] = False
            response_data['message'] = 'Book borrow details could not be entered'

        if response_data['status_code'] == '400':
            resp_status = status.HTTP_400_BAD_REQUEST
        elif response_data['status_code'] == '201':
            resp_status = status.HTTP_201_CREATED

        return Response(response_data, status=resp_status)