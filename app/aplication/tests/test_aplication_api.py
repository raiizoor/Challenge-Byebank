from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Modalidade, Ativo, Aplicacao


APLICACAO_URL = reverse('aplicacao:aplicacao')


def sample_ativos(user, **params):
    """Create and return sample ativos"""
    defaults = {
        'name': 'Investimento em Bitcoin',
    }
    defaults.update(params)

    return Ativo.objects.create(user=user, **defaults)


class PublicAplicacaoApiTests(TestCase):
    """Test the publicly available aplicação API"""

    def setUp(self):
        self.client = APIClient()

    def test_loggin_required(self):
        """Test login is required to access the endpoints"""
        response = self.client.get(APLICACAO_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAplicacaoApiTests(TestCase):
    """Test the private available aplicação API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test12345'
        )
        self.client.force_authenticate(self.user)
    
    def test_create_aplicacao_to_failed(self):
        """Test to create new aplicação failed"""
        payload = {
            'value': '500',
            'ativos': '',
        }

        response = self.client.post(APLICACAO_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_aplicacao_successful(self):
        """Test to create aplicação success"""
        ativos = sample_ativos(user=self.user)
        payload = {
            'value': '500',
            'ativos': ativos.id,
        }

        response = self.client.post(APLICACAO_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
