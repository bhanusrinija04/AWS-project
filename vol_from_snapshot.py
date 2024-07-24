"""
Your module description
"""
import boto3
import botocore
import time

ec2_client = boto3.client('ec2')

def validate_snapshot_id(snapshot_id):
    try:
        response = ec2_client.describe_snapshots(SnapshotIds=[snapshot_id])
        if response['Snapshots']:
            return True
        else:
            print(f'Snapshot ID {snapshot_id} is not found.')
            return False
    except botocore.exceptions.ClientError as error:
        print(f'Error describing snapshot: {error}')
        return False

def wait_for_snapshot_to_be_completed(snapshot_id):
    if not validate_snapshot_id(snapshot_id):
        raise ValueError(f'Snapshot ID {snapshot_id} is invalid.')

    while True:
        try:
            response = ec2_client.describe_snapshots(SnapshotIds=[snapshot_id])
            snapshot_state = response['Snapshots'][0]['State']
            if snapshot_state == 'completed':
                print(f'Snapshot {snapshot_id} is completed.')
                return
            elif snapshot_state == 'error':
                print(f'Snapshot {snapshot_id} is in error state.')
                raise Exception(f'Snapshot {snapshot_id} failed.')
            else:
                print(f'Snapshot {snapshot_id} is still {snapshot_state}. Waiting...')
                time.sleep(30)  # Wait for 30 seconds before checking again
        except botocore.exceptions.ClientError as error:
            print(f'Error checking snapshot status: {error}')
            raise

def create_volume_from_snapshot(snapshot_id, availability_zone):
    try:
        wait_for_snapshot_to_be_completed(snapshot_id)

        new_volume = ec2_client.create_volume(
            SnapshotId=snapshot_id,
            AvailabilityZone=availability_zone,
            VolumeType='gp2'  # You can specify other volume types if needed
        )
        print(f'New volume created with ID: {new_volume["VolumeId"]}')
        return new_volume["VolumeId"]
    except botocore.exceptions.ClientError as error:
        print(f'Error creating volume from snapshot: {error}')
        raise

def wait_for_volume_to_be_available(volume_id):
    while True:
        try:
            response = ec2_client.describe_volumes(VolumeIds=[volume_id])
            volume_state = response['Volumes'][0]['State']
            if volume_state == 'available':
                print(f'Volume {volume_id} is available.')
                return
            else:
                print(f'Volume {volume_id} is still {volume_state}. Waiting...')
                time.sleep(10)  # Wait for 10 seconds before checking again
        except botocore.exceptions.ClientError as error:
            print(f'Error checking volume status: {error}')
            raise

def attach_volume_to_instance(volume_id, instance_id, device):
    try:
        response = ec2_client.attach_volume(
            VolumeId=volume_id,
            InstanceId=instance_id,
            Device=device
        )
        print(f'Volume {volume_id} attached to instance {instance_id} as {device}')
    except botocore.exceptions.ClientError as error:
        print(f'Error attaching volume: {error}')
        raise

# Example usage
snapshot_id = 'snap-00b94f4a19d3a3c98'  # Replace with your snapshot ID
availability_zone = 'us-east-1d'  # Replace with the appropriate availability zone
instance_id = 'i-09d49cf4902369524'  # Replace with your instance ID
device = '/dev/sdf'  # Replace with the appropriate device name

try:
    new_volume_id = create_volume_from_snapshot(snapshot_id, availability_zone)
    print(f'Volume created from snapshot {snapshot_id} with ID: {new_volume_id}')
    
    # Wait for the new volume to become available
    wait_for_volume_to_be_available(new_volume_id)
    
    # Attach the new volume to the instance
    attach_volume_to_instance(new_volume_id, instance_id, device)
except Exception as e:
    print(f'Failed to create volume from snapshot: {e}')
