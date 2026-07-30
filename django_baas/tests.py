from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import EntitySchema, EntityRecord
from .serializers import EntityRecordSerializer


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


class EntitySerializerTestCase(TestCase):


    def setUp(self):
        self.product_schema = EntitySchema.objects.create(
            name = 'Product',
            fields_definition = {
                'type': 'object',
                'properties': {
                    'title': {'type':'string'},
                    'price': {'type':'integer', 'minimum':0}
                },
                'required': ['title', 'price'],
            } 
        )


    def test_serializer_with_valid_data(self):
        payload = {
            'schema': self.product_schema.id,
            'data': {'title': 'Laptop', 'price':500}
        }

        serializer = EntityRecordSerializer(data=payload)

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()
        self.assertEqual(instance.data['title'], payload['data']['title'])
        self.assertEqual(instance.data['price'], payload['data']['price'])


    def test_serializer_with_invalid_data(self):
        payload = {
            'schema': self.product_schema.id,
            'data': {'title': 'Phone', 'price': -50}
        }
        
        serializer = EntityRecordSerializer(data=payload)
        
        self.assertFalse(serializer.is_valid())
        
        error_message = str(serializer.errors['data'][0])
        self.assertIn("-50 is less than the minimum of 0", error_message)

    def test_serializer_missing_required_field(self):
        payload = {
            'schema': self.product_schema.id,
            'data': {'title': 'Book'}
        }
        
        serializer = EntityRecordSerializer(data=payload)
        
        self.assertFalse(serializer.is_valid())
        
        error_message = str(serializer.errors['data'][0])
        self.assertIn("'price' is a required property", error_message)