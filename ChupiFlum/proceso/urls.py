from django.conf.urls import url, include
from rest_framework import routers
from .views import ProcesoViewSet

router = routers.DefaultRouter()
router.register(r'procesos', ProcesoViewSet, base_name='procesos')

urlpatterns = [
    url(r'^', include(router.urls)),
]
