from django.db import models
from django.contrib.auth.models import User
import random

class EmailConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def random_code(self):
        self.code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.save()

    





