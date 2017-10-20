from django.conf.urls import url, include
from rest_framework import routers
from .views import GroupViewSet


router = routers.DefaultRouter()
router.register(r'grupos', GroupViewSet, 'group')

urlpatterns = [
    url(r'^', include(router.urls)),
]
