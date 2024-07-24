import boto3
from botocore.exceptions import ClientError

def detach_volume(volume_id, instance_id):
    """
    Detach an EBS volume from an EC2 instance.

    :param volume_id: The ID of the EBS volume
    :param instance_id: The ID of the EC2 instance from which to detach the volume
    :return: True if the volume was successfully detached, else False
    """
    ec2_client = boto3.client('ec2')
    
    try:
        # Detach the volume
        response = ec2_client.detach_volume(
            VolumeId=volume_id,
            InstanceId=instance_id
        )
        # Optionally, you can wait for the volume to be detached
        waiter = ec2_client.get_waiter('volume_available')
        waiter.wait(VolumeIds=[volume_id])
        print(f'Volume {volume_id} has been detached from instance {instance_id}.')
        return True
    except ClientError as e:
        print(f'Error: {e}')
        return False

# Specify your details
volume_id = 'vol-0cd4f8a9461bf8cb2'  # Replace with your EBS volume ID
instance_id = 'i-09d49cf4902369524'  # Replace with your EC2 instance ID

# Detach the volume
detach_volume(volume_id, instance_id)
