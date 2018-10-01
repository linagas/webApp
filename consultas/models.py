from django.db import models
import requests
REMOTE_API_URL = "https://api.sbif.cl/api-sbifv3/recursos_api/uf/?apikey=551dd58d90fca467536cde1c80dc3728d7030876&"
JSON = 'json'
# Create your models here.

class ApiClient(models.Model):
    id = models.AutoField(primary_key=True)
    apikey = models.CharField(max_length=100)

    def get_in_period(self, *args, **kwargs):
        data = {'year': self.year, 'month': self.month}
        response = requests.get(REMOTE_API_URL+ data['year'] +data['month'])
        return response