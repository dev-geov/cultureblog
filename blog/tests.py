from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Category, BlogUser


class TestBlog(TestCase):

    def setUp(self):

        self.category = Category(
            name='category 1',
        )
        self.category.save()

        self.user = User(
            email='geapsi@gmail.com',
            first_name='Geovani',
            last_name='Silva',
            username='geapsi'
        )
        self.user.save()

        self.blog_user = BlogUser(
            user=self.user,
            writer=True,
        )
        self.blog_user.save()


    def test_blog_posts_index(self):
        response = self.client.get(reverse('blog:posts-index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])
    
    def test_blog_post_detail(self):
        post = Post(
            title='Teste 1 title',
            content='Test 1 content',
            author=self.blog_user,
            publish=True,
        )
        post.save()
        post.category.add(self.category)

        response = self.client.get(reverse('blog:post-detail', kwargs={'slug': post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["post"], post)
