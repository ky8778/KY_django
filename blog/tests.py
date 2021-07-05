from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import Post, Category, Tag
from bs4 import BeautifulSoup

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        # Client 선언
        self.client = Client()

        # user 생성
        self.user_one = User.objects.create_user(username='one', password='one1')
        self.user_two = User.objects.create_user(username='two', password='two2')
        
        # category 생성
        self.category_game = Category.objects.create(name='game', slug='game')
        self.category_music = Category.objects.create(name='music', slug='music')
        
        # Tag 생성
        self.tag_test = Tag.objects.create(name='testtag', slug='testtag')
        self.tag_game = Tag.objects.create(name='gametag', slug='gametag')
        self.tag_music = Tag.objects.create(name='musictag', slug='musictag')

        # Post가 3개 생성
        self.post_001 = Post.objects.create(
            title='Test1',
            content='Test1',
            category=self.category_game,
            author=self.user_one,
        )
        self.post_001.tags.add(self.tag_game)
        
        self.post_002 = Post.objects.create(
            title='Test2',
            content='Test2',
            category=self.category_music,
            author=self.user_two,
        )
        self.post_002.tags.add(self.tag_music)
        self.post_003.tags.add(self.tag_test)

        self.post_003 = Post.objects.create(
            title='Test3',
            content='Test3',
            # no category
            author=self.user_one,
        )


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


    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_game.name} : {self.category_game.post_set.count()}', categories_card.text)
        self.assertIn(f'{self.category_music.name} : {self.category_music.post_set.count()}', categories_card.text)
        self.assertIn(f'미분류 : 1', categories_card.text)


    def test_post_list(self):
        # Post 3개
        self.assertEqual(Post.objects.count(), 3)

        # Post List Page 가져오기
        response = self.client.get('/blog/')
        # Page Load Success
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Page Tilte : Blog
        self.assertEqual(soup.title.text, 'Blog')
        
        # navbar 에 Blog, About Me 확인
        self.navbar_test(soup)
        # Category Test
        self.category_card_test(soup)

        # main area에 게시글 없을 경우, '아직 게시물이 없습니다' 문구
        main_area = soup.find('div', id='main-area')
        if Post.objects.count() == 0:
            self.assertIn('아직 게시물이 없습니다.', main_area.text)
        else:
            self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        # main area에 Post 3개 Test
        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_music, post_001_card.text)
        self.assertNotIn(self.tag_game, post_001_card.text)
        self.assertNotIn(self.tag_test, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_music, post_002_card.text)
        self.assertIn(self.tag_game, post_002_card.text)
        self.assertIn(self.tag_test, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_music, post_003_card.text)
        self.assertNotIn(self.tag_game, post_003_card.text)
        self.assertNotIn(self.tag_test, post_003_card.text)

        # Author
        self.assertIn(self.user_one.username.upper(), main_area.text)
        self.assertIn(self.user_two.username.upper(), main_area.text)

        # Post 없는경우 만들어서 Test
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        # Post List Page 새로고침
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # main area에 게시글 없을 경우, '아직 게시물이 없습니다' 문구
        main_area = soup.find('div', id='main-area')
        if Post.objects.count() == 0:
            self.assertIn('아직 게시물이 없습니다.', main_area.text)
        else:
            self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        # Post url : '/blog/1/'
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # Post Detail Page Test
        # 1. URL status_code 200 : 정상
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2. navbar 확인
        self.navbar_test(soup)

        # 3. Post title 확인
        self.assertIn(self.post_001.title, soup.title.text)

        # 4. Post title post_area에 존재
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_game.name, post_area.text)

        # 5. content 확인
        self.assertIn(self.post_001.content, post_area.text)

        # 6. author 확인
        self.assertIn(self.user_one.username.upper(), main_area.text)
    
    def test_category_page(self):
        response = self.client.get(self.category_game.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_game.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_game.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)