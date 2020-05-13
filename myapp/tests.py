from django.test import TestCase, RequestFactory
from django.test import Client
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import logout
from django.conf import settings
from . import models
from . import forms
from .views import index, submit, viewissues, viewmyissues, \
self_assign, register, logoff, profile_page, edit_profile, \
become_technician, view_technicians, view_profile, viewmysubmittedissues, \
edit_review, resolve_ticket, edit_ticket, about
from model_mommy import mommy

# Create your tests here.


class AuthTests(TestCase):
    def test_registration(self):
        c = Client()
        response = c.post('/register/', {'username': 'tester', 'email': 'tester@testing.test', 'password': 'testingtesting123'})
        self.assertEqual(200, response.status_code)

    def test_registration_then_login(self):
        c = Client()
        response = c.post('/register/', {'username': 'tester', 'email': 'tester@testing.test', 'password': 'testingtesting123'})
        response = c.post('/login/', {'username': 'tester', 'password': 'testingtesting123'})
        self.assertEqual(200, response.status_code)


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="passwordlol", first_name="user")

    def test_issue_form_valid(self):
        data = {'title': "Test", 'description': "test", 'issue_type': "Desktop", 'is_solved': 0}
        form = forms.IssueForm(data=data)
        self.assertTrue(form.is_valid())

    def test_issue_form_invalid(self):
        data = {'title': "", 'description': "", 'issue_type': "", 'is_solved': ""}
        form = forms.IssueForm(data=data)
        self.assertFalse(form.is_valid())

    def test_issue_filter_valid(self):
        data = {'keyword': "test", 'issue_type': "Desktop"}
        form = forms.IssueFilter(data=data)
        self.assertTrue(form.is_valid())

    def test_profile_form_valid(self):
        data = {"email": "test@test.com", "bio": "test", "location": "test"}
        form = forms.ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_profile_form_nontech_valid(self):
        data = {"email": "test@test.com"}
        form = forms.ProfileFormNontech(data=data)
        self.assertTrue(form.is_valid())

    def test_profile_filter_valid(self):
        data = {'keyword': "test", 'name': "test", 'location': "test"}
        form = forms.IssueFilter(data=data)
        self.assertTrue(form.is_valid())

    def test_add_review_form_valid(self):
        data = {'rating': 5, 'review': "test", 'writer': self.user}
        form = forms.AddReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_review_form_invalid(self):
        data = {'rating': "", 'review': "test", 'writer': ""}
        form = forms.AddReviewForm(data=data)
        self.assertFalse(form.is_valid())

    def test_edit_review_form_valid(self):
        data = {'rating': 5, 'review': "test", 'writer': self.user}
        form = forms.EditReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_edit_review_form_invalid(self):
        data = {'rating': "", 'review': "test", 'writer': ""}
        form = forms.EditReviewForm(data=data)
        self.assertFalse(form.is_valid())

    def test_resolveissue_form_valid(self):
        data = {'resolution': "I fixed the thing."}
        form = forms.ResolveIssueForm(data=data)
        self.assertTrue(form.is_valid())

    def test_editissue_form_valid(self):
        data = data = {'title': "Test", 'description': "test", 'issue_type': "Desktop", 'is_solved': 0}
        form = forms.EditIssueForm(data=data)
        self.assertTrue(form.is_valid())

    def test_editissue_form_invalid(self):
        data = data = {'title': "", 'description': "", 'issue_type': "", 'is_solved': ""}
        form = forms.EditIssueForm(data=data)
        self.assertFalse(form.is_valid())


class ModelTests(TestCase):
    def test_issue_creation(self):
        new_issue = mommy.make(models.Issue_Model)
        self.assertTrue(isinstance(new_issue, models.Issue_Model))
        self.assertEqual(new_issue.__unicode__(), new_issue.title)

    # Currently has issues testing due to a OneToOneField preventing us
    # from creating a Profile model for testing. Current coverage is at
    # 98% because of this.

    # def test_profile_creation(self):
    #    new_profile = mommy.make(models.Profile)
    #    self.assertTrue(isinstance(new_profile, models.Profile))
    #    self.assertEqual(new_profile.__unicode__(), new_profile.user)

    def test_reivew_creation(self):
        new_review = mommy.make(models.Review)
        self.assertTrue(isinstance(new_review, models.Review))
        self.assertEqual(new_review.__unicode__(), new_review.writer)


class ViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@test.com', password='supersecretpass')
        self.user_id = self.user.id

    def test_index_view_authenticated(self):
        request = self.factory.get('/index.html')
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200) 
    
    def test_index_view_unauthenticated(self):
        request = self.factory.get('/index.html')
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 200) 
    
    def test_submit_view(self):
        request = self.factory.get('/submit.html')
        request.user = self.user
        response = submit(request)
        self.assertEqual(response.status_code, 200) 

    def test_view_issues(self):
        request = self.factory.get('/viewissues.html')
        request.user = self.user
        response = viewissues(request) 
        self.assertEqual(response.status_code, 200)

    def test_view_my_submitted_issues(self):
        request = self.factory.get('/viewmysubmittedissues.html')
        request.user = self.user
        response = viewmysubmittedissues(request) 
        self.assertEqual(response.status_code, 200)

    def test_view_edit_ticket(self):
        request = self.factory.get('/editticket/1')
        request.user = self.user
        response = edit_ticket(request, 1) 
        self.assertEqual(response.status_code, 302)  # we're checking to see if this page exists

    def test_view_edit_review(self):
        request = self.factory.get('/editreview/1')
        request.user = self.user
        response = edit_review(request, self.user_id) 
        self.assertEqual(response.status_code, 302)

    def test_view_my_issues(self):
        request = self.factory.get('/viewmyissues.html')
        request.user = self.user
        response = viewmyissues(request) 
        self.assertEqual(response.status_code, 200)

    def test_view_technicians(self):
        request = self.factory.get('/viewtechnicians.html')
        request.user = self.user
        response = view_technicians(request) 
        self.assertEqual(response.status_code, 200)

    def test_view_about_authenticated(self):
        request = self.factory.get('/aboutodit.html')
        request.user = self.user
        response = about(request) 
        self.assertEqual(response.status_code, 200)
    
    def test_view_about_unauthenticated(self):
        request = self.factory.get('/aboutodit.html')
        request.user = AnonymousUser()
        response = about(request) 
        self.assertEqual(response.status_code, 200)

    def test_view_profile(self):
        request = self.factory.get('/profile.html')
        request.user = self.user
        response = view_profile(request, self.user_id) 
        self.assertEqual(response.status_code, 200)

    def test_view_edit_profile(self):
        request = self.factory.get('/profile/edit.html')
        request.user = self.user
        response = edit_profile(request) 
        self.assertEqual(response.status_code, 200)

    def test_view_login(self):
        c = Client()
        response = c.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_register(self):
        request = self.factory.get('/register/')
        response = register(request) 
        self.assertEqual(response.status_code, 200)

    def test_view_self_assign(self):
        request = self.factory.get('/viewissues/assign/1')
        request.user = self.user
        response = self_assign(request, 1)
        self.assertEqual(response.status_code, 302)
    
    def test_view_profile_page(self):
        request = self.factory.get('/profile.html')
        request.user = self.user
        response = profile_page(request)
        self.assertEqual(response.status_code, 200)
    
    def test_view_become_technician(self):
        request = self.factory.get('/profile/becometechnician')
        request.user = self.user
        response = become_technician(request)
        self.assertEqual(response.status_code, 302)
    
    def test_view_resolve_ticket(self):
        request = self.factory.get('/resolve/1')
        request.user = self.user
        response = resolve_ticket(request, 1)
        self.assertEqual(response.status_code, 302)
