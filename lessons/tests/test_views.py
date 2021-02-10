from django.test import TestCase


class TestLessonViews(TestCase):

    def test_get_lessons(self):
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')

    def test_subscibe_to_lesson(self):
        