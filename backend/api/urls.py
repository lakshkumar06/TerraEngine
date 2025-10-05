from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mars-sites', views.MarsSiteViewSet, basename='mars-sites')
router.register(r'crops', views.MarsCropViewSet, basename='crops')
router.register(r'regions', views.MarsRegionViewSet, basename='regions')

urlpatterns = [
    path('', include(router.urls)),
]
