from django.conf.urls import url, include
from rest_framework import routers
from .views import GroupViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'groups', GroupViewSet, 'group')

urlpatterns = [
    url(r'^', include(router.urls)),
]
