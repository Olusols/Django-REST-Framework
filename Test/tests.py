from urllib import response
from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from . import views
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class PollTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = views.PollViewSet.as_view({
            'get': 'list',
        })
        self.uri = 'polls/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        
        
    @staticmethod
    def setup_user():
        
        User = get_user_model()
        user  = User.objects.create_user(
            'test',
            
            email='test@gmail.com', 
            password = 'test'
        )
        return user
    
    
        
    def test_list(self):
        request = self.factory.get(self.uri,
              HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        request.user  = self.user
        response = self.view(request)
        comment = 'Expected Response code 200, {} received'.format(response.status_code)
        self.assertEqual(response.status_code, 200, comment)

    
        
    def test_list3(self):
       self.client.login(username="test", password="test")
       response = self.client.get(self.uri)
       self.assertEqual(response.status_code, 200,
                'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    def test_list2(self):
        
        self.client.login(username="test", password="test")
        response = self.client.get(self.uri)
        
       
        comment = 'Expected Response code 200, {} received'.format(response.status_code)
        self.assertEqual(response.status_code, 200, comment)