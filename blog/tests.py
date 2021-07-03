from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import Post
from bs4 import BeautifulSoup

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_one = User.objects.create_user(username='one', password='one1')
        self.user_two = User.objects.create_user(username='two', password='two2')

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        head_btn = navbar.find('a', text='KY')
        self.assertEqual(head_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):
        # Post List Page 가져오기
        response = self.client.get('/blog/')
        # Page Load Success
        self.assertEqual(response.status_code, 200)
        # Page Tilte : Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # navbar 에 Blog, About Me 확인
        self.navbar_test(soup)
        
        # Post가 없는 경우
        self.assertEqual(Post.objects.count(), 0)
        # main area에 '아직 게시물이 없습니다' 문구
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # Post가 2개 생성
        post_001 = Post.objects.create(
            title='Test1',
            content='Test1',
            author=self.user_one,
        )
        post_002 = Post.objects.create(
            title='Test2',
            content='Test2',
            author=self.user_two,
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

        # Author
        self.assertIn(self.user_one.username.upper(), main_area.text)
        self.assertIn(self.user_two.username.upper(), main_area.text)
        
    def test_post_detail(self):
        # Post 1개 생성
        post_001 = Post.objects.create(
            title='test1',
            content='text1',
            author=self.user_one,
        )
        # Post url : '/blog/1/'
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # Post Detail Page Test
        # 1. URL status_code 200 : 정상
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2. navbar 확인
        self.navbar_test(soup)

        # 3. Post title 확인
        self.assertIn(post_001.title, soup.title.text)

        # 4. Post title post_area에 존재
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 5. content 확인
        self.assertIn(post_001.content, post_area.text)

        # 6. author 확인
        self.assertIn(self.user_one.username.upper(), main_area.text)