from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth import get_user_model

class TestSetup(APITestCase):
  def setUp(self):
    self.login_url = reverse("token_obtain_pair")
    self.refresh_url = reverse("token_refresh")
    self.logout_url = reverse("logout")
    # set default users
    self.default_users = {}
    print(f"________________________________________________\n\n")
    for _ in range(10):
      if _ == 0:
        self.default_users[_] = {
          "email": "tombra4ril@gmail.com",
          "password": "asdf;lkj"
        }
      else:
        fake_user = Faker()
        self.default_users[_] = {
          "email": fake_user.email(),
          "password": fake_user.password()
        }
        print(f"email = {self.default_users[_]['email']} \npassword = {self.default_users[_]['password']}\n")
    # save users in database
    user = get_user_model()
    for _ in self.default_users.keys():
      new_user = user.objects.create_user(email=self.default_users[_]["email"], password=self.default_users[_]["password"])
    return super().setUp()

  def tearDown(self):
    return super().tearDown()