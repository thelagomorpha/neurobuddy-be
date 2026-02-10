from django.test import TestCase
from .models import Message


class MessageModelTest(TestCase):
    def setUp(self):
        Message.objects.create(content="Test message")
    
    def test_message_creation(self):
        """Test that a message can be created"""
        message = Message.objects.get(content="Test message")
        self.assertEqual(message.content, "Test message")
        self.assertIsNotNone(message.created_at)


class HelloWorldViewTest(TestCase):
    def test_hello_world_endpoint(self):
        """Test the hello world endpoint"""
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertIn('database_connected', response.json())
    
    def test_messages_list_endpoint(self):
        """Test the messages list endpoint"""
        Message.objects.create(content="Test message 1")
        Message.objects.create(content="Test message 2")
        
        response = self.client.get('/api/messages/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('count', data)
        self.assertEqual(data['count'], 2)
