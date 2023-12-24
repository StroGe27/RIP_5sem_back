from django.db import models
from django.contrib.auth.models import PermissionsMixin , UserManager, AbstractBaseUser

class NewUserManager(UserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email адрес"), unique=True)
    password = models.CharField(max_length=255, verbose_name="Пароль")    
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    full_name = models.CharField(max_length=255, default='', verbose_name='ФИО')
    phone_number = models.CharField(max_length=30, default='', verbose_name='Номер телефона')

    USERNAME_FIELD = 'email'

    objects =  NewUserManager()

    

class Requests_status(models.Model):
    name_status = models.CharField(max_length=30)
    class Meta:
        managed = True
        db_table = 'requests_status'
    def __str__(self):
        return self.name_status

class Requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_create = models.DateField()
    date_formation = models.DateField()
    date_complete = models.DateField()
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    status = models.ForeignKey('Requests_status', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.status, self.date_complete
    class Meta:
        managed = True
        db_table = 'requests'
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

class Order_to_request(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE)
    request = models.ForeignKey('Requests', on_delete=models.CASCADE)
    amount_months = models.IntegerField()
    class Meta:
        managed = True
        db_table = 'order_to_request' 
 
class Orders(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    processor = models.CharField(max_length=100)
    ghz = models.FloatField()
    ram = models.IntegerField()
    availableos = models.ForeignKey('AvailableOS', on_delete=models.CASCADE)
    cost = models.IntegerField()
    ip = models.CharField(max_length=20)
    img = models.CharField(max_length=20)
    processor_type = models.ForeignKey('Processor', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title, self.status
    class Meta:
        managed = True
        db_table = 'orders' 
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
 
class AvailableOS(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        managed = True
        db_table = 'availableos' 
    def __str__(self):
        return self.name

class Processor(models.Model):
    name = models.CharField(max_length=10)
    class Meta:
        managed = True
        db_table = 'processor' 