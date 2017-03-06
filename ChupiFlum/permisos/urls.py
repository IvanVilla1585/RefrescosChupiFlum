from django.conf.urls import url, include
from rest_framework import routers
from permisos.views import PermisosViewSet

router = routers.DefaultRouter()
router.register(r'permisos', PermisosViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]