from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Item

class PostModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Item.objects.create(
            buyer = test_user,
            item_name = 'Title of Blog',
            item_description = 'Words about the blog'
        )
        test_post.save()

    def test_blog_content(self):
        item = Item.objects.get(id=1)

        self.assertEqual(str(item.buyer), 'tester')
        self.assertEqual(item.item_name, 'Title of Blog')
        self.assertEqual(item.item_description, 'Words about the blog')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_item = Item.objects.create(
            buyer = test_user,
            item_name = 'Title of Blog',
            item_description = 'Words about the blog'
        )
        test_item.save()

        response = self.client.get(reverse('item_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'item_name': test_item.item_name,
            'item_description': test_item.item_description,
            'buyer': test_user.id,
        })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        url = reverse('item_list')
        data = {
            "item_name":"Testing is Fun!!!",
            "item_description":"when the right tools are available",
            "buyer":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().item_name, data['item_name'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Item.objects.create(
            buyer = test_user,
            item_name = 'Title of Blog',
            item_description = 'Words about the blog'
        )

        test_post.save()

        url = reverse('item_detail',args=[test_post.id])
        data = {
            "item_name":"Testing is Still Fun!!!",
            "buyer":test_post.buyer.id,
            "item_description":test_post.item_description,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Item.objects.count(), test_post.id)
        self.assertEqual(Item.objects.get().item_name, data['item_name'])


    def test_delete(self):
        """Test the api can delete a post."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_item = Item.objects.create(
            buyer = test_user,
            item_name = 'Title of Blog',
            item_description = 'Words about the blog'
        )

        test_item.save()

        item = Item.objects.get()

        url = reverse('item_detail', kwargs={'pk': item.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)