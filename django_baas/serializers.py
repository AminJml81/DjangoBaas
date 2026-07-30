from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import EntitySchema, EntityRecord


class EntitySchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntitySchema    
        fields = ['id', 'name', 'slug', 'fields_definition', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class EntityRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntityRecord
        fields = ['id', 'schema', 'data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


    def validate(self, attrs):
        instance = EntityRecord(**attrs)
        try:
            instance.full_clean(exclude=['id'])
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs