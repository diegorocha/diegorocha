from model_mommy import mommy
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse


class HomeTest(TestCase):
    def test_home(self):
        response = self.client.get(reverse('curriculo:home'))
        self.assertEquals(response.status_code, 200)


class NotFoundTest(TestCase):
    def test_invalid_url(self):
        response = self.client.get('/foobar')
        self.assertEquals(response.status_code, 404)


class SendContactViewTest(TestCase):
    def setUp(self):
        self.url = reverse('curriculo:send-contact')
        self.post_data = {'from_email': 'foo@bar.com', 'subject': 'Teste', 'message': 'Foo bar'}
        self.profile = mommy.make('curriculo.Profile', _fill_optional=True, make_m2m=True)

    def test_send_contact_ok(self):
        with self.settings(USE_SMTP=False):
            self.assertEqual(settings.USE_SMTP, False)
            response = self.client.post(self.url, self.post_data)
            self.assertEquals(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])

    def test_send_contact_force_exception(self):
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'):
            self.assertEqual(settings.EMAIL_BACKEND, 'django.core.mail.backends.smtp.EmailBackend')
            response = self.client.post(self.url, self.post_data)
            self.assertEquals(response.status_code, 400)
            data = response.json()
            self.assertFalse(data["success"])
            self.assertIsNotNone(data["error"])

    def test_send_contact_no_from(self):
        post_data = self.post_data
        post_data.pop('from_email')
        response = self.client.post(self.url, post_data)
        self.assertEquals(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])

    def test_send_contact_no_subject(self):
        post_data = self.post_data
        post_data.pop('subject')
        response = self.client.post(self.url, post_data)
        self.assertEquals(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])

    def test_send_contact_no_message(self):
        post_data = self.post_data
        post_data.pop('message')
        response = self.client.post(self.url, post_data)
        self.assertEquals(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])

    def test_send_contact_no_data(self):
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
