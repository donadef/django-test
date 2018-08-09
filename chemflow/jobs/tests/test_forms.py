from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Job
User = get_user_model()


class JobTestCase(TestCase):
    def setUp(self):
        super(JobTestCase, self).setUp()

        self.user = User.objects.create(username='testuser', password='12345')

    # def test_create_job(self):
    #     job = Job(project_name="test", protocol="test", sf= "mmgbsa", receptor_file="file", ligands_file="file")
    #     job.save()
    #
    #     Job.objects.get(pk=1)

    def test_create_job_through_form(self):
        c = Client()
        c.force_login(user=self.user)

        data1 = {
            "project_name": "test",
            "protocol": "test",
            "sf": "vina",
            "receptor_file": "/home/donadef/Downloads/Screenshot.png",
            "ligands_file": "/home/donadef/Downloads/Screenshot.png",
        }

        response = c.post(reverse('jobs:create_dock'), data=data1)
        # response = self.client.get(reverse('carmanager:saveNewDriverInfo'), data={
        #     'form': {'carID': '1034567', 'Driver_Last_Name': 'daddy', 'Driver_First_Name': 'daddy',
        #              'Driver_Middle_Initial': 'K', 'entered_by': 'king'}})
        # self.assertRedirects(response, expected_url, status_code, target_status_code, host, msg_prefix, fetch_redirect_response)
        print(response.context['form'].errors)
        self.assertRedirects(response, '/jobs/')

        data2 = {
            "project_name": "test",
            "protocol": "test",
            "sf": "vina",
            "receptor_file": "/home/donadef/Downloads/Screenshot.png",
            "ligands_file": "/home/donadef/Downloads/Screenshot.png",
        }

        response = c.post(reverse('jobs:create_dock'), data=data2)
        # Job.objects.get()
        #
        # response = c.post('/jobs/new', data=data)
        print(response.context['form'].errors)
        # print(response.context['form']['sf'].data)
        # print(type(response.context['form']['sf']))
        # self.assertNotContains(response, 'something went wrong', 200)
