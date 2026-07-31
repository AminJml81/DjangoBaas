from rest_framework import viewsets

from .models import EntitySchema, EntityRecord
from .serializers import EntitySchemaSerializer, EntityRecordSerializer


class EntitySchemaViewSet(viewsets.ModelViewSet):

    queryset = EntitySchema.objects.all().order_by('-created_at')
    serializer_class = EntitySchemaSerializer


class EntityRecordViewSet(viewsets.ModelViewSet):

    queryset = EntityRecord.objects.all().order_by('-created_at')
    serializer_class = EntityRecordSerializer