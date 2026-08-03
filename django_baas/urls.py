from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import EntitySchemaViewSet, EntityRecordViewSet

router = DefaultRouter()
router.register(r'schemas', EntitySchemaViewSet, basename='schema')
router.register(r'records', EntityRecordViewSet, basename='record')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(router.urls)),
]
