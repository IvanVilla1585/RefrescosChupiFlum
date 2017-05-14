from django.conf.urls import url, include
from rest_framework import routers
from .views import CategoriaMateriaPrimaViewSet

router = routers.DefaultRouter()
router.register(r'categoriamateria', CategoriaMateriaPrimaViewSet, base_name='categoriamateria')

urlpatterns = [
    url(r'^', include(router.urls)),
]
