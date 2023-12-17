from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .config import LIBVIRT_CREDENTIALS
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer
from .libvirtconnect import Connection  

@api_view(['GET'])
def list_vms(request):
    """
    API endpoint to list virtual machines using libvirt.
    """
    try:
        # Create an instance of the Connection class
        conn_instance = Connection()

        # Connect to libvirt
        conn_instance.connect()

        # Get all domain IDs
        domain_ids = conn_instance.conn.listDomainsID()

        vm_list = []

        for domain_id in domain_ids:
            # Look up each domain by ID
            domain = conn_instance.conn.lookupByID(domain_id)

            # Get information about the virtual machine's disk
            disk_info = domain.blockInfo('vda')  # 'vda' is an example, adjust it based on your setup
            disk_data = {
                'disk_size': disk_info[0] / (1024 ** 3),  # Disk size in GB
                'allocated_space': disk_info[1] / (1024 ** 3)  # Allocated space in GB
            }

            vm_data = {
                'id': domain.ID(),
                'name': domain.name(),
                'state': domain.state()[0],
                'vcpus': domain.info()[3],  # Number of virtual CPUs
                'memory': domain.info()[1] / 1024,  # Memory size in MB
                'autostart': domain.autostart(),
                'uuid': domain.UUIDString(),  # XML description of the domain
                'storage_info': disk_data
            }
            vm_list.append(vm_data)

        return Response(vm_list)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        if conn_instance.conn is not None:
            conn_instance.conn.close()


            
@api_view(['POST'])
def create_vm(request):
    """
    API endpoint to create a new virtual machine using libvirt.
    """
    try:
        # Create an instance of the Connection class
        conn_instance = Connection()

        # Connect to libvirt (automatically fetches credentials from config.py)
        conn_instance.connect()

        # Parse input data using the updated serializer
        serializer = CreateVMSerializer(data=request.data)
        if serializer.is_valid():
            vm_name = serializer.validated_data['name']
            memory = serializer.validated_data['memory']
            vcpus = serializer.validated_data['vcpus']
            storage_size = serializer.validated_data['storage_size']

            # Add logic for VM creation based on your requirements
            new_vm_xml = f'''
                <domain type='qemu'>
                    <name>{vm_name}</name>
                    <memory unit='KiB'>{memory * 1024}</memory>
                    <vcpu placement='static'>{vcpus}</vcpu>
                    <!-- Add other necessary elements for storage, network, etc. -->
                </domain>
            '''
            
            new_vm = conn_instance.conn.createXML(new_vm_xml, 0)

            if new_vm is not None:
                return Response({'message': f'Virtual machine {vm_name} created successfully'})
            else:
                return Response({'error': f'Failed to create virtual machine {vm_name}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        if conn_instance.conn is not None:
            conn_instance.conn.close()


@api_view(['DELETE'])
def delete_vm(request, vm_id):
    try:
        # Create an instance of the Connection class
        conn_instance = Connection()

        # Connect to libvirt
        conn_instance.connect()

        # Look up the virtual machine by ID
        domain = conn_instance.conn.lookupByID(vm_id)
        domain.shutdown()
        domain.undefine()

        return Response({'message': f'Virtual machine {vm_id} deleted successfully'})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        if conn_instance.conn is not None:
            conn_instance.conn.close()