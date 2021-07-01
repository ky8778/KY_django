from django.test import TestCase, Client
from .models import Post
from bs4 import BeautifulSoup

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # Post List Page 가져오기
        response = self.client.get('/blog/')
        # Page Load Success
        self.assertEqual(response.status_code, 200)
        # Page Tilte : Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # navbar 확인
        navbar = soup.nav
        # navbar 에 Blog, About Me 확인
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # Post가 없는 경우
        self.assertEqual(Post.objects.count(), 0)
        # main area에 '아직 게시물이 없습니다' 문구
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        