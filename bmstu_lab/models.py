from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=30)
    mail = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField()
    who_moderator = models.ForeignKey('Moderators', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'users'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    

class Moderators(models.Model):
    name = models.CharField(max_length=30)
    mail = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'moderators'

class Requests(models.Model):
    status = models.CharField(max_length=10)
    date_create = models.DateField()
    date_formation = models.DateField()
    date_complete = models.DateField()
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    moderator = models.ForeignKey('Moderators', on_delete=models.CASCADE)
    def __str__(self):
        return self.status, self.date_complete
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'request'
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class Orders(models.Model):
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    processor = models.CharField(max_length=100)
    ghz = models.FloatField()
    ram = models.IntegerField()
    availableos = models.CharField(max_length=10)
    cost = models.IntegerField()
    ip = models.CharField(max_length=16)
    cluster = models.IntegerField()
    
    def __str__(self):
        return self.title, self.status
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'orders' 
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
 

class Clusters(models.Model):
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=255)