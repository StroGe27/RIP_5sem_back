from api import views
from django.urls import include, path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework import routers
from rest_framework import permissions

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
   path('', include(router.urls)),
   # Набор методов для услуг 
   path('api/orders/', views.OrderList.as_view()),  # GET
   path('api/orders/search/', views.OrderSearch),  # GET
   path('api/orders/<int:id>/', views.OrderDetail.as_view()), # GET | PUT | DELETE

   # Набор методов для заявок
   path('api/requests/', views.RequestList.as_view()), # GET
   path('api/requests/<int:id>/', views.RequestDetail.as_view()), # GET | PUT | DELETE
   # path('api/requests/<int:id>/update_status_user/', views.UpdateStatusUser.as_view()),  # PUT
   # path('api/requests/<int:id>/update_status_admin/', views.UpdateStatusAdmin.as_view()),  # PUT


   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

   # Авторизация
   path('login',  views.login_view, name='login'),
   path('logout', views.logout_view, name='logout'),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


   # path(r'users/', views.User.as_view()),
   # path(r'requests/<int:id>/', views.RequestDetail.as_view(), name="requests-detail"),
]