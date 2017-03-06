from django.conf.urls import url, include
from rest_framework import routers
from permisos.views import PermisosViewSet
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'permisos', PermisosViewSet, base_name='permissions')

urlpatterns = [
    url(r'^', include(router.urls)),
]
