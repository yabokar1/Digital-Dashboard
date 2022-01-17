from django.db import reset_queries
from django.test import TestCase
from .models import Districts
from django.conf import settings 
from django.contrib.auth.models import User
from django.test import Client
# Create your tests here.

class TestCases(TestCase):

    # Creating test rows in test District table
    def setUp(self):    
        # Districts.objects.all()
        settings.DEBUG = True
        Districts.objects.create(district_id=201, state="California", locale="rural", pct_black_hispanic=0.9, county_connection=0.56, pp_total_raw=0.18)
        Districts.objects.create(district_id=202, state="Illinois", locale="urban", pct_black_hispanic=0.8, county_connection=0.66, pp_total_raw=0.30)

    def test_district_graph_information(self):
        o = Districts.objects.all()
        s = "California"
        county_connections = []
        list_of_objects_in_a_state =  Districts.objects.filter(state=s).count()

        for item in o:
            if (item.county_connection):
                county_connections.append(item.county_connection)
       
        self.assertEqual(len(county_connections), 2)                                    # Testing if length of county_connections array is 2 as there are 2 objects/rows in table
        
        for i in county_connections:
            self.assertGreaterEqual(i, 0.0000000000000001)                              # Testing if no value is negative as negative values are not allowed.

    
    def test_user_login(self):
        user = User.objects.create(username='testuser')                                 # Creating a test user
        user.set_password('thisismytestpassword')
        user.save()

        c = Client()
        login_success = c.login(username='testuser', password='thisismytestpassword')   # Testing with correct password
        login_fail = c.login(username='testuser', password='hi')                        # Testing with incorrect password
        self.assertTrue(login_success, True)
        self.assertFalse(login_fail, False)


        
