from django.db import models
from django.db.models import JSONField
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex


class EntitySchema(models.Model):
    """Schema for storing Tables structure"""
    name = models.CharField(max_length=100, unique=True,)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
        
    fields_definition = JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entity Schema"
        verbose_name_plural = "Entity Schemas"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"


class EntityRecord(models.Model):
    """Stores actual record data for a schema"""
    schema = models.ForeignKey(
        EntitySchema, 
        on_delete=models.CASCADE, 
        related_name='records'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    data = JSONField(default=dict)
    is_deleted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entity Record"
        verbose_name_plural = "Entity Records"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['schema', 'is_deleted', '-created_at']),
            GinIndex(fields=['data'], name='entity_record_data_gin'),
        ]

    def __str__(self):
        return f"Record #{self.id} for {self.schema.name}"