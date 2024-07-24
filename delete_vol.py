import boto3
import time
from botocore.exceptions import ClientError, EndpointConnectionError

# Initialize a session using your AWS credentials
session = boto3.Session(
    aws_access_key_id='AKIA6GBMDP6LOW4Z4EWM',
    aws_secret_access_key='nLL75KkttSfke75d1NwW36P9jIJHQfTy7Xnx99kO',
    region_name='us-east-1'  # Use a valid region name
)

# Create an EC2 resource
ec2 = session.resource('ec2')

# Volume ID you want to delete
volume_id = 'vol-0cd4f8a9461bf8cb2'  # Replace with your volume ID

try:
    # Get the volume
    volume = ec2.Volume(volume_id)

    # Check if the volume is attached to any instance
    if volume.state == 'in-use':
        # Detach the volume if it's in use
        volume.detach_from_instance(InstanceId=volume.attachments[0]['InstanceId'])
        print(f'Detaching volume {volume_id}...')
        
        # Wait until the volume is detached
        while volume.state != 'available':
            time.sleep(5)
            volume.reload()
            print('Waiting for volume to detach...')

    # Now delete the volume
    volume.delete()
    print(f'Volume {volume_id} has been deleted.')

except ClientError as e:
    print(f'ClientError: {e}')
except EndpointConnectionError as e:
    print(f'EndpointConnectionError: {e}')
except Exception as e:
    print(f'Unexpected error: {e}')
