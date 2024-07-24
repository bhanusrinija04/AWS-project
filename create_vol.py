import boto3
import time

def create_volume(availability_zone, size, volume_type='gp2'):
    ec2 = boto3.client('ec2')
    print("Creating volume...")
    
    response = ec2.create_volume(
        AvailabilityZone=availability_zone,
        Size=size,
        VolumeType=volume_type
    )
    
    volume_id = response['VolumeId']
    print(f"Volume {volume_id} created. Waiting for it to become available...")

    # Wait for the volume to become available
    waiter = ec2.get_waiter('volume_available')
    waiter.wait(VolumeIds=[volume_id])

    print(f"Volume {volume_id} is now available.")
    return volume_id

def wait_for_volume_available(volume_id, timeout=300, interval=5):
    ec2 = boto3.client('ec2')
    elapsed_time = 0
    
    while elapsed_time < timeout:
        response = ec2.describe_volumes(VolumeIds=[volume_id])
        volume_state = response['Volumes'][0]['State']
        
        if volume_state == 'available':
            print(f"Volume {volume_id} is available.")
            return True
        
        print(f"Volume {volume_id} state: {volume_state}. Waiting...")
        time.sleep(interval)
        elapsed_time += interval
    
    print(f"Timeout waiting for volume {volume_id} to become available.")
    return False

def attach_volume(instance_id, volume_id, device):
    ec2 = boto3.client('ec2')
    print("Attaching volume...")
    
    response = ec2.attach_volume(
        InstanceId=instance_id,
        VolumeId=volume_id,
        Device=device
    )
    
    print("Volume attached:", response)
    return response

if __name__ == '__main__':
    # Specify your details
    availability_zone = 'us-east-1d'  # Replace with your availability zone
    instance_id = 'i-09d49cf4902369524'  # Replace with your actual instance ID
    size = 10  # Size in GiB
    device = '/dev/sdf'  # Ensure this is an unused device name on your instance
    
    # Create a new EBS volume
    volume_id = create_volume(availability_zone, size)
    print(f'Volume {volume_id} created successfully.')
    
    # Ensure the volume is available before attaching
    if wait_for_volume_available(volume_id):
        # Attach the new volume to the instance
        attach_response = attach_volume(instance_id, volume_id, device)
        print(f'Volume {volume_id} attached to instance {instance_id} as {device}.')
    else:
        print(f'Failed to attach volume {volume_id} to instance {instance_id} due to availability timeout.')
