from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EntitySchema, EntityRecord
from .serializers import EntityRecordSerializer


class EntityValidationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product_schema = EntitySchema.objects.create(
            user=self.user,
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
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product_schema = EntitySchema.objects.create(
            user = self.user,
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


class EntityAPIViewSetTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.schema = EntitySchema.objects.create(
            user=self.user,
            name='TestProduct',
            fields_definition={
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'price': {'type': 'integer', 'minimum': 0}
                },
                'required': ['title', 'price']
            }
        )
        self.schema_id = self.schema.id

        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.other_schema = EntitySchema.objects.create(
            user=self.other_user,
            name='OtherUserProduct',
            fields_definition={'type': 'object'}
        )

    def test_create_schema_via_api(self):
        payload = {
            'name': 'Customer',
            'fields_definition': {
                'type': 'object',
                'properties': {'name': {'type': 'string'}}
            }
        }

        response = self.client.post(reverse('schema-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Customer')
        self.assertIn('id', response.data)


    def test_create_valid_record_via_api(self):
        payload = {
            'schema': self.schema_id,
            'data': {'title': 'Monitor', 'price': 300}
        }
        
        response = self.client.post(reverse('record-list'), payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], payload['data']['title'])
        self.assertEqual(response.data['data']['price'], payload['data']['price'])


    def test_create_invalid_record_via_api(self):
        payload = {
            'schema': self.schema_id,
            'data': {'title': 'Keyboard', 'price': -10}
        }
        
        response = self.client.post(reverse('record-list'), payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('data', response.data)
        error_message = str(response.data['data'][0])
        self.assertIn("-10 is less than the minimum of 0", error_message)


    def test_cannot_create_record_for_other_users_schema(self):
        payload = {
            'schema': self.other_schema.id,
            'data': {}
        }

        response = self.client.post(reverse('record-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)