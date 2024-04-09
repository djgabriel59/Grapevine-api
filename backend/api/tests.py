from django.test import Client, TestCase

# Create your tests here.

class CreateUserTest(TestCase):
    def setUp(self):
        self.clinet = Client()

    def test_create_user(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_password',
        }
        response = self.client.post('/api/user/register/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_users(self):
        response = self.clinet.get('/api/user/register/')
        self.assertEqual(response.status_code, 200)
