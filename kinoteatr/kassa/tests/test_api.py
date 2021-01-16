import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from kassa.models import Film
from kassa.serializers import FilmSerializer


class FilmApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.film_1 = Film.objects.create(name='Test film 1', price=25, author_name='Author_1', owner=self.user)
        self.film_2 = Film.objects.create(name='Test film 2', price=25, author_name='Author_2', owner=self.user)
        self.film_3 = Film.objects.create(name='Test film 1', price=55, author_name='Author_34', owner=self.user)
        self.film_4 = Film.objects.create(name='Test film 2', price=55, author_name='Author_4 last text for searching', owner=self.user)

    def test_get(self):
        """Тест на получение данных"""
        url = reverse('film-list')  # либо film-detail для получения конкретной
        response = self.client.get(url)
        serializer_data = FilmSerializer([self.film_1, self.film_2, self.film_3, self.film_4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data,
                         response.data)  # many используется чтобы дать понять, что надо сериализовать каждый объект

    def test_create(self):
        """Тест на создание данных"""
        self.assertEqual(4, Film.objects.all().count())
        self.client.force_login(self.user)
        url = reverse('film-list')  # либо film-detail для получения конкретной
        data={
            "name": "Profi Python 4",
            "price": "1500.00",
            "author_name": "LuC"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, Film.objects.all().count())
        self.assertEqual(self.user, Film.objects.last().owner)

    # def test_delete(self):
    #     self.client.force_login(self.user)
    #     url = reverse('film-detail')
    #     responce =self.client.delete(url, )

    def test_update(self):
        """Тест на обновление данных с правильным пользователем"""
        url = reverse('film-detail', args=(self.film_1.id,))
        data = {
            "name": self.film_1.name,
            "price": 15,
            "author_name": self.film_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.film_1.refresh_from_db()
        self.assertEqual(15, self.film_1.price)

    def test_update_not_owner(self):
        """Тест на то, что пользователь НЕправильный"""
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('film-detail', args=(self.film_1.id,))
        data = {
            "name": self.film_1.name,
            "price": 15,
            "author_name": self.film_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.', code='permission_denied')}, response.data)
        self.film_1.refresh_from_db()
        self.assertEqual(25, self.film_1.price)

    def test_update_not_owner_but_staff(self):
        """Тест на то, что пользователь НЕправильный"""
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('film-detail', args=(self.film_1.id,))
        data = {
            "name": self.film_1.name,
            "price": 15,
            "author_name": self.film_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.film_1.refresh_from_db()
        self.assertEqual(15, self.film_1.price)

    def test_get_filter(self):
        """Тест фильтрации данных"""
        url = reverse('film-list')  # либо film-detail для получения конкретной
        response = self.client.get(url, data={'price': 55})
        serializer_data = FilmSerializer([self.film_3, self.film_4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data,response.data)

    def test_get_search(self):
        """Тест проверки поиска данных"""
        url = reverse('film-list')
        responce = self.client.get(url, data={'search': '4'})
        serializer_data = FilmSerializer([self.film_3, self.film_4], many=True).data
        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(serializer_data, responce.data)
