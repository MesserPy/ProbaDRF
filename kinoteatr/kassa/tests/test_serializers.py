from unittest import TestCase

from django.contrib.auth.models import User

from kassa.models import Film


#TODO разобраться почему не идёт тест
from kassa.serializers import FilmSerializer


class FilmSerializerTestCase(TestCase):
    def test_film(self):
        user = User.objects.create(username='test_serialize')
        film_1 = Film.objects.create(name='Test film 1', price=25, author_name="Author 1", owner=user)
        film_2 = Film.objects.create(name='Test film 2', price=25, author_name="Author 2", owner=user)

        data = FilmSerializer([film_1, film_2],many=True).data

        expected_data = [
            {
                'id':film_1.id,
                'name':'Test film 1',
                'price': '25.00',
                'author_name': "Author 1",
                'owner' : user.id,
            },
            {
                'id':film_2.id,
                'name': 'Test film 2',
                'price': '25.00',
                'author_name': "Author 2",
                'owner' : user.id,
            },
        ]

        self.assertEqual(expected_data, data)
