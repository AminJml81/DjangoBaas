from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import EntitySchemaViewSet, EntityRecordViewSet

router = DefaultRouter()
router.register(r'schemas', EntitySchemaViewSet, basename='schema')
router.register(r'records', EntityRecordViewSet, basename='record')


urlpatterns = [
    path('', include(router.urls)),
]
