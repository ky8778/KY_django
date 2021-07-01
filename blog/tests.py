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

        # Post가 2개 생성
        post_001 = Post.objects.create(
            title='Test1',
            content='Test1',
        )
        post_002 = Post.objects.create(
            title='Test2',
            content='Test2',
        )
        self.assertEqual(Post.objects.count(), 2)

        # Post List Page 새로고침
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # main area에 Post 2개 제목 존재
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # '아직 게시물이 없습니다.' 문구 이제 없음.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
        