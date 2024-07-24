import boto3
from botocore.exceptions import ClientError

def create_snapshot(volume_id, description='Snapshot created by boto3'):
    """
    Create a snapshot of an EBS volume.

    :param volume_id: The ID of the EBS volume
    :param description: Description of the snapshot
    :return: Snapshot ID if creation was successful, else None
    """
    ec2_client = boto3.client('ec2')
    
    try:
        response = ec2_client.create_snapshot(
            VolumeId=volume_id,
            Description=description
        )
        snapshot_id = response['SnapshotId']
        print(f'Snapshot {snapshot_id} created for volume {volume_id}.')
        return snapshot_id
    except ClientError as e:
        print(f'Error: {e}')
        return None

# Specify the volume ID for which you want to create a snapshot
volume_id = 'vol-0cd4f8a9461bf8cb2'  # Replace with your specific volume ID

# Create a snapshot for the specified volume
create_snapshot(volume_id, 'Snapshot of volume created by boto3')
