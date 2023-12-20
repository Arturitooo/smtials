from django.test import TestCase
from django.contrib.auth.models import User
from .models import RetrospectiveBoard, RetroTicket

# Create your tests here.

class RetrospectiveBoardTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_board_successfully(self):
        # Create board request
        response = self.client.post(
            '/retro/api/retrospective-board/',
            {'owner': self.user.id, 'name': 'Test Board', 'variant': 'Good / Bad'},
        )
        # Check if the response status is 201 (created)
        self.assertEqual(response.status_code, 201)
        # Check if the board is created
        self.assertEqual(RetrospectiveBoard.objects.count(), 1)

    def test_create_board_without_login(self):
        # Create a user
        self.client.logout()

        # Attempt to create a RetrospectiveBoard instance without being logged in
        response = self.client.post(
            '/retro/api/retrospective-board/',
            {'owner': self.user.id, 'name': 'Test Board', 'variant': 'Good / Bad'},
        )

        # Check if the response status is 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)
        # Check if the board is not created
        self.assertEqual(RetrospectiveBoard.objects.count(), 0)

    def test_create_board_without_name(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Attempt to create a RetrospectiveBoard instance without providing a name (invalid)
        response = self.client.post(
            '/retro/api/retrospective-board/',
            {'owner': self.user.id, 'variant': 'Good / Bad'},
        )

        # Check if the response status is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        # Check if the board is not created
        self.assertEqual(RetrospectiveBoard.objects.count(), 0)

    def test_create_board_too_long_name(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Attempt to create a RetrospectiveBoard instance without providing a name (invalid)
        response = self.client.post(
            '/retro/api/retrospective-board/',
            {'owner': self.user.id, 'name':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries...",  'variant': 'Good / Bad'},
        )
        # Check if the response status is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        # Check if the board is not created
        self.assertEqual(RetrospectiveBoard.objects.count(), 0)

class RetroTicketTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_ticket_successfully(self):
        # Creating a user
        board = RetrospectiveBoard.objects.create(
            owner=self.user,
            name='Test Board',
            variant='Good / Bad',
        )        
        # Create a Retro ticket instance
        response = self.client.post(
            '/retro/api/retro-tickets/',
            {'author': self.user.id, 'board': board.id, 'ticket_type': 'Good', 'content': 'Test Content'},
        )
        # Check if the response status is 201 (Created)
        self.assertEqual(response.status_code, 201)
        # Check if the board is created
        self.assertEqual(RetroTicket.objects.count(), 1)

    def test_create_ticket_without_login(self):
        # Creating a user
        board = RetrospectiveBoard.objects.create(
            owner=self.user,
            name='Test Board',
            variant='Good / Bad',
        )
        self.client.logout()
        

        # Create a Retro ticket instance
        response = self.client.post(
            '/retro/api/retro-tickets/',
            {'author': self.user.id, 'board': board.id, 'ticket_type': 'Good', 'content': 'Test Content'},
        )

        # Check if the response status is 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)

        # Check if the board is not created
        self.assertEqual(RetroTicket.objects.count(), 0)