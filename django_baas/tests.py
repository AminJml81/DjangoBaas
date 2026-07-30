from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import EntitySchema, EntityRecord


class EntityValidationTestCase(TestCase):

    def setUp(self):
        self.product_schema = EntitySchema.objects.create(
            name='Product',
            fields_definition={
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'price': {'type': 'integer', 'minimum': 0}
                },
                'required': ['title', 'price'],
            }
        )

    def test_valid_record_data(self):
        record = EntityRecord(
            schema=self.product_schema,
            data={'title': 'Laptop', 'price': 1500}
        )
        record.full_clean()

    def test_invalid_negative_price(self):
        record = EntityRecord(
            schema=self.product_schema,
            data={'title': 'Phone', 'price': -100}
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_invalid_string_price(self):
        record = EntityRecord(
            schema=self.product_schema,
            data={'title': 'Phone', 'price': 'twenty'}
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_invalid_float_price(self):
        record = EntityRecord(
            schema=self.product_schema,
            data={'title': 'Phone', 'price': 1000.3}
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_invalid_integer_title(self):
        record = EntityRecord(
            schema=self.product_schema,
            data={'title': 123, 'price': 1000.3}
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_missing_required_title_field(self):
        record = EntityRecord(
            schema=self.product_schema,
            data={'title': 'Book'}
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_missing_required_title_field(self):
        record = EntityRecord(
            schema=self.product_schema,
            data={'price': 123}
        )
        with self.assertRaises(ValidationError):
            record.full_clean()