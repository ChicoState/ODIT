from django.test import TestCase
from django.test import Client
from myapp import models

# Create your tests here.
c = Client()
response = c.post('/register/', {'username': 'tester', 'email': 'tester@testing.test', 'password': 'testingtesting123'})
print('Status code:',response.status_code)
print('Content:',response.content)
response = c.post('/login/', {'username': 'tester', 'password': 'testingtesting123'})
print('Status code:',response.status_code)
print('Content:',response.content)