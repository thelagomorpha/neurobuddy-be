from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from unittest.mock import patch

from .models import Message


class MessageModelTest(TestCase):
    def setUp(self):
        Message.objects.create(content="Test message")
    
    def test_message_creation(self):
        """Test that a message can be created"""
        message = Message.objects.get(content="Test message")
        self.assertEqual(message.content, "Test message")
        self.assertIsNotNone(message.created_at)

    def test_message_str_truncates(self):
        long_content = "X" * 60
        message = Message.objects.create(content=long_content)
        self.assertEqual(str(message), f"Message {message.id}: {long_content[:50]}")


class HelloWorldViewTest(TestCase):
    def test_hello_world_endpoint(self):
        """Test the hello world endpoint"""
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertIn('database_connected', response.json())

    @patch('api.views.Message.objects.count', side_effect=Exception("db error"))
    @patch('api.views.connection.cursor')
    def test_hello_world_db_error(self, mock_cursor, _mock_count):
        mock_cursor.side_effect = Exception("db down")
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['database_connected'])
        self.assertIn('Database connection error', data['database_message'])
        self.assertEqual(data['total_messages'], 0)
    
    def test_messages_list_endpoint(self):
        """Test the messages list endpoint"""
        Message.objects.create(content="Test message 1")
        Message.objects.create(content="Test message 2")
        
        response = self.client.get('/api/messages/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('count', data)
        self.assertEqual(data['count'], 2)

    def test_messages_create_endpoint(self):
        response = self.client.post(
            '/api/messages/',
            data='{ "content": "New message" }',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['content'], 'New message')

    def test_messages_create_requires_content(self):
        response = self.client.post(
            '/api/messages/',
            data='{ "content": "" }',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_messages_create_invalid_json(self):
        response = self.client.post(
            '/api/messages/',
            data='not-json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


class SeedDataCommandTest(TestCase):
    def test_seed_data_command(self):
        call_command('seed_data')
        self.assertEqual(Message.objects.count(), 5)


class EntryPointTest(SimpleTestCase):
    def test_asgi_application_import(self):
        from backend.asgi import application as asgi_app
        self.assertIsNotNone(asgi_app)

    def test_wsgi_application_import(self):
        from backend.wsgi import application as wsgi_app
        self.assertIsNotNone(wsgi_app)


class ManagePyTest(SimpleTestCase):
    def test_manage_py_main(self):
        from importlib import reload
        import manage

        with patch('django.core.management.execute_from_command_line') as mock_exec:
            reload(manage)
            manage.main()
            mock_exec.assert_called_once()
