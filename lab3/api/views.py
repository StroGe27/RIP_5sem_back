from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets

#API
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from api.serializers import *
from api.models import Orders, Requests, CustomUser
from api.permissions import *

#For auth

#Swagger
from drf_yasg.utils import swagger_auto_schema


# поменять
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.conf import settings
import redis
import uuid
from django.contrib.sessions.models import Session

from minio import Minio
from minio.error import S3Error
from datetime import datetime

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class OrderList(APIView):
    model_class = Orders
    serializer_class = OrderSerializer

    def get(self, request, format=None):
        orders = self.model_class.objects.filter(status='valid')
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)
    
    @permission_classes([IsManager])
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    model_class = Orders
    serializer_class = OrderSerializer

    def get(self, request, id, format=None):
        order = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(order)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        order = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        order = get_object_or_404(self.model_class, id=id)
        order.status = "deleted"
        order.save()        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])   
def OrderSearch(request):
    search_query = request.GET.get('title', '')  # Пример GET запроса: /your-endpoint/?search=ваша_строка&
    proc_type = request.GET.get('type', '')

    left_cost = request.GET.get('lcost', '') 
    right_cost = request.GET.get('rcost', '')
    orders = Orders.objects.filter(status='valid')
    orders = orders.filter(title__icontains=search_query)
    if proc_type == "Intel":
        orders = orders.filter(processor_type_id=1)
    elif proc_type == "AMD":
        orders = orders.filter(processor_type_id=2)

    print(proc_type, left_cost, right_cost)
    # orders = orders.filter(cost__range=(int(left_cost), int(right_cost)))

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class RequestList(APIView):
    model_class = Requests
    serializer_class = RequestSerializer
    
    def get(self, request, format=None):
        request = self.model_class.objects.all().order_by('date_create')
        serializer = self.serializer_class(request, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestDetail(APIView):
    model_class = Requests
    serializer_class = RequestSerializer

    def get(self, request, id, format=None):
        requests = get_object_or_404(self.model_class.objects.all(), id=id)
        serializer = self.serializer_class(requests)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        requests = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(requests, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        requests = get_object_or_404(self.model_class, id=id)
        requests.status_id = 2  # обновляем статус на deleted
        requests.save()   
        return Response(status=status.HTTP_204_NO_CONTENT)

# Authorization methods
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        print('req is', request.data)
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.model_class.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     full_name=serializer.data['full_name'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, serializer.data['email'])
            user_data = {
                "email": request.data['email'],
                "full_name": request.data['full_name'],
                #"phone_number": request.data['phone_number'],
                "is_superuser": False
            }

            print('user data is ', user_data)
            response = Response(user_data, status=status.HTTP_201_CREATED)
            # response = HttpResponse("{'status': 'ok'}")
            response.set_cookie("session_id", random_key)
            return response
            # return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=username, password=password)
    if user is not None:
        print(user)
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        user_data = {
            "id_user": user.id_user,
            "email": user.email,
            "full_name": user.full_name,
            #"phone_number": user.phone_number,
            "password": user.password,
            #"is_superuser": user.is_superuser,
        }
        response = Response(user_data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, samesite="Lax", max_age=30 * 24 * 60 * 60)
        return response
    else:
        return HttpResponse("login failed", status=400)

@api_view(['POST'])
@permission_classes([IsAuth])
def logout_view(request):
    ssid = request.COOKIES["session_id"]
    if session_storage.exists(ssid):
        session_storage.delete(ssid)
        response_data = {'status': 'Success'}
    else:
        response_data = {'status': 'Error', 'message': 'Session does not exist'}
    return Response(response_data)

@api_view(['GET'])
# @permission_classes([IsAuth])
def user_info(request):
    try:
        ssid = request.COOKIES["session_id"]
        if session_storage.exists(ssid):
            email = session_storage.get(ssid).decode('utf-8')
            user = CustomUser.objects.get(email=email)
            user_data = {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_superuser": user.is_superuser
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'})
    except:
        return Response({'status': 'Error', 'message': 'Cookies are not transmitted'})