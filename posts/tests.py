from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')


    def test_Can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    


class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Post.objects.create(
            owner=adam, title='a title', content='adam content'
            )
        Post.objects.create(
            owner=brian, title='another title', content='brian content'
            )    

    def test_can_get_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_get_post_with_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_update_post_if_logged_in(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'edit title'}) 
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'edit title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_canNOT_update_post_if_not_owner(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'edit brian title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)   