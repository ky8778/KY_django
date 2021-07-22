from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from blog.models import Post


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_one = User.objects.create_user(username='one', password='pw1')

    def test_home(self):
        post_001 = Post.objects.create(
            title='post1',
            content='post1',
            author=self.user_one
        )

        post_002 = Post.objects.create(
            title='post2',
            content='post2',
            author=self.user_one
        )

        post_003 = Post.objects.create(
            title='post3',
            content='post3',
            author=self.user_one
        )
        
        post_004 = Post.objects.create(
            title='post4',
            content='post4',
            author=self.user_one
        )

        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.body
        self.assertNotIn(post_001.title, body.text)
        self.assertIn(post_002.title, body.text)
        self.assertIn(post_003.title, body.text)
        self.assertIn(post_004.title, body.text)