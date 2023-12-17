from rest_framework import serializers
from .models import VirtualMachine

class VirtualMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMachine
        fields = '__all__'
