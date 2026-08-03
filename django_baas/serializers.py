from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import PermissionDenied

from .models import EntitySchema, EntityRecord


class EntitySchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntitySchema    
        fields = ['id', 'user', 'name', 'slug', 'fields_definition', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'slug', 'created_at', 'updated_at']


class EntityRecordSerializer(serializers.ModelSerializer):
    schema = serializers.PrimaryKeyRelatedField(queryset=EntitySchema.objects.all())

    class Meta:
        model = EntityRecord
        fields = ['id', 'schema', 'data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


    def validate(self, attrs):
        request = self.context.get('request')
        schema = attrs.get('schema')

        if request and schema and schema.user != request.user:
            raise PermissionDenied("You are not allowed to add records to other users schemas.")
        
        instance = EntityRecord(**attrs)
        try:
            instance.full_clean(exclude=['id'])
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs