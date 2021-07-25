from .test_setup import TestSetup
from django.contrib.auth import get_user_model

class TestViews(TestSetup):
  debug_functions = {
    1: {
        "function": "test_login_with_no_data",
        "debug": False,
    },
    2: {
        "function": "test_login_with_no_password",
        "debug": False,
    },
    3: {
        "function": "test_login_with_no_email",
        "debug": False,
    },
    4: {
        "function": "test_login",
        "debug": False,
    },
  }

  def test_login_with_no_data(self):
    """ Checks if a user can log in without any data """
    response = self.client.post(self.login_url)
    #
    if self.debug_functions[1]["debug"]:
      import pdb
      pdb.set_trace()
    #
    self.assertEqual(response.status_code, 400)

  def test_login_with_no_password(self):
    """ Checks if a user can log in without a password """
    user_data = self.default_users[0]
    user_data["password"] = ""
    response = self.client.post(self.login_url, user_data, format="json")
    #
    if self.debug_functions[2]["debug"]:
      import pdb
      pdb.set_trace()
    #
    self.assertEqual(response.status_code, 400)

  def test_login_with_no_email(self):
    """ Checks if a user can log in without an email """
    user_data = self.default_users[1]
    user_data["email"] = ""
    response = self.client.post(self.login_url, user_data, format="json")
    #
    if self.debug_functions[3]["debug"]:
      import pdb
      pdb.set_trace()
    #
    self.assertEqual(response.status_code, 400)

  def test_login(self):
    """ Checks if a user can log in with data """
    # first create a default user
    # create the user before verifying the user
    user_data = self.default_users[2]
    # self.create_users()
    # login
    response = self.client.post(self.login_url, user_data, format="json")
    #
    if self.debug_functions[4]["debug"]:
      import pdb
      pdb.set_trace()
    #
    self.assertEqual(response.status_code, 200)

  def create_users(self):
    """ This is used to create a default user """
    user = get_user_model()
    new_user = user.objects.create_user(email=self.default_users["email"], password=self.default_users["password"])
