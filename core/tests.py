from django.test import TestCase
from .models import Post

# Create your tests here.


class PostTest(TestCase):
    """
    Defining test , we will run for Post Model
    """
    def test_str(self):
        test_name = Post(name='A Post')
        self.assertEqual(str(test_name), 'A Post')
