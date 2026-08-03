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

    ordering_fields = ['created_at', 'updated_at', 'schema_id']
    filterset_fields = ['schema']

    def get_queryset(self):
        queryset =  EntityRecord.objects.filter(schema__user=self.request.user)

        json_filters = {}
        for key, value in self.request.query_params.items():
            if key.startswith('data__'):
                json_filters[key] = value

        if json_filters:
            queryset = queryset.filter(**json_filters)

        return queryset