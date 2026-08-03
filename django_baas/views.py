from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import EntitySchema, EntityRecord
from .serializers import EntitySchemaSerializer, EntityRecordSerializer


class EntitySchemaViewSet(viewsets.ModelViewSet):
    serializer_class = EntitySchemaSerializer

    def get_queryset(self):
        return EntitySchema.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EntityRecordViewSet(viewsets.ModelViewSet):
    serializer_class = EntityRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EntityRecord.objects.filter(schema__user=self.request.user)