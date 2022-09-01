from django.test import TestCase as Test, Client
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.urls import reverse
from . import models

# Create your tests here.

class PostTest(Test):
    
    def setUp(self) -> None:
        
        user1 = get_user_model().objects.create_user(username="user1", email="", password="p1")
        user2 = get_user_model().objects.create_user(username="user2", email="", password="p2")
        user3 = get_user_model().objects.create_user(username="user3", email="", password="p3")
        user1.save()
        user2.save()
        user3.save()
        
        client1 = models.Client(user=user1)
        client2 = models.Client(user=user2)
        client1.save()
        client2.save()
        
        post1 = models.Post(topic="test1", content="content Test")
        post1.save()
        post1.authors.add(client1)
        post1.authors.add(client2)
        
    def test_ClientCreation(self):
        """test whether Client is unique
        """
        
        user = get_user_model().objects.get(username="user1")
        self.assertRaises(IntegrityError, models.Client.objects.create, user=user)
     
    def test_redirect(self):
        
        addresses = ["index", "addPost", "logout"]
        c = Client()
        
        for url in addresses:
            response = c.get(reverse(url))
            self.assertEqual(response.status_code, 302)
        
    def test_login(self):
        #c = Client()
        #response = c.post("login", {"username":"user1", "password":"p1"})
        pass

        
    
    def test_creating_Post(self):
        c = Client()
        c.login(username="user2", email="", password="p2")
        
        response: HttpResponse = c.post("/addPost", {"topic":"test", "content":"this is a test"})
        
        self.assertEqual(response.status_code, 200)
        
        testPost = models.Post.objects.get(topic="test")
        self.assertEqual(testPost.content, "this is a test")
        self.assertEqual(testPost.authors.all()[0].user.username, "user2")
        
