from django.conf.urls import url, include
from rest_framework import routers
from .views import LoginUserApi



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'sigin', LoginUserApi, 'sigin')

urlpatterns = [
    url(r'^', include(router.urls)),
]
