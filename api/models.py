from django.db import models

class VirtualMachine(models.Model):
    name = models.CharField(max_length=255)
    memory = models.IntegerField()
    vcpu = models.IntegerField()
    # Add other fields as needed
