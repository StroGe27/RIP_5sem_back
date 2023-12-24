from api.models import Orders
from api.models import Requests
from api.models import CustomUser
from rest_framework import serializers

class RequestSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=False)  #чтобы можно было добавлять с произвольным id
    class Meta:
        # Модель, которую мы сериализуем
        model = Requests
        # Поля, которые мы сериализуем
        fields = ["date_create", "date_formation", "date_complete", "moderator", "user", "status"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Orders
        # Поля, которые мы сериализуем
        fields = ["id", "title", "status", "processor", "ghz", "ram", "ip", "processor_type_id", "availableos", "cost", "img"]

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email',
                  'password',
                  'full_name',
                  'phone_number',
                  'is_staff',
                  'is_superuser']

# from collections import OrderedDict
# class OrdersSerializer(serializers.ModelSerializer):
#     class Meta:
#         # Модель, которую мы сериализуем
#         model = Orders
#         # Поля, которые мы сериализуем
#         fields = ["id", "title", "status", "processor", "ghz", "ram", "ip", "processor_type_id", "availableos", "cost", "img"]

#         def get_fields(self):
#             new_fields = OrderedDict()
#             for name, field in super().get_fields().items():
#                 field.required = False
#                 new_fields[name] = field
#             return new_fields 

