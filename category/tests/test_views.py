from rest_framework.test import (
  APIRequestFactory,
  APITestCase
)
from category.views import (
  CategoryListView,
)
from django.urls import reverse
import json

class CategoryListViewTest(APITestCase):
  """
    This test all the functions in the CategoryListView whether or not they return the correct data from the database.
  """
  def setUp(self):
    pass
    # self.factory = RequestFactory()
    # self.api_factory = APIRequestFactory()
    self.url = reverse("category_category_list_view")
    self.response = self.client.get(self.url)

  def test_get_with_status_code_200(self):
    ## create an instance of a GET reguest
    # request = self.factory.get(reverse("category_category_list_view"))
    ## because my view is classed based, i will use the method below
    # response = CategoryListView.as_view()(request)
    ## check what it returns
    # self.assertEqual(response.status_code, 200)
    """
      tests whether the status code of the response is 200
    """
    self.assertEqual(self.response.status_code, 200)

  def test_get_with_correct_response_data(self):
    data = {
      "categories": [
        {"id": 1, "name": "Doctor"},
        {"id": 2, "name": "Nurse"},
        {"id": 3, "name": "Pharmacist"},
        {"id": 4, "name": "Laboratorist"},
        {"id": 5, "name": "Accountant"},
        {"id": 6, "name": "Patient"},
        {"id": 7, "name": "Admin"},
      ]
    }
    self.assertEqual(json.loads(self.response.content), data)