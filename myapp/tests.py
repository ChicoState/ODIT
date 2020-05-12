from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from . import models
from . import forms
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
    # Utilizing status code 302 for pages that require authentication. HTTP code
    # 302 indicates the requested page was found. This code is used mainly
    # for redirects, but in our case a code of 302 indicates that the page is found
    # but the user cannot view it due to the '@login_required' decorators
    # we have placed over particular functions.

    def test_index_view(self):
        c = Client()
        response = c.get('/index.html')
        self.assertEqual(response.status_code, 200)

    def test_submit_view(self):
        c = Client()
        response = c.get('/submit.html')
        self.assertEqual(response.status_code, 302)

    def test_view_issues(self):
        c = Client()
        response = c.get('/viewissues.html')
        self.assertEqual(response.status_code, 302)

    def test_view_my_submitted_issues(self):
        c = Client()
        response = c.get('/viewmysubmittedissues.html')
        self.assertEqual(response.status_code, 302)

    def test_view_edit_ticket(self):
        c = Client()
        response = c.get('/editticket/1')
        self.assertEqual(response.status_code, 302)

    def test_view_edit_review(self):
        c = Client()
        response = c.post('/editreview/1', {'rating': 5, 'review': "you rock!"})
        self.assertEqual(response.status_code, 302)

    def test_view_my_issues(self):
        c = Client()
        response = c.get('/viewmyissues.html')
        self.assertEqual(response.status_code, 302)

    def test_view_technicians(self):
        c = Client()
        response = c.get('/viewtechnicians.html')
        self.assertEqual(response.status_code, 302)

    def test_view_about(self):
        c = Client()
        response = c.get('/aboutodit.html')
        self.assertEqual(response.status_code, 200)

    def test_view_profile(self):
        c = Client()
        response = c.get('/profile.html')
        self.assertEqual(response.status_code, 302)

    def test_view_edit_profile(self):
        c = Client()
        response = c.get('/profile/edit.html')
        self.assertEqual(response.status_code, 302)

    def test_view_login(self):
        c = Client()
        response = c.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_register(self):
        c = Client()
        response = c.get('/register/')
        self.assertEqual(response.status_code, 200)
