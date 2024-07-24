import os
import subprocess

def is_mounted(device, mount_point):
    """Check if the device is already mounted."""
    try:
        result = subprocess.check_output(['mount'])
        return f'{device} on {mount_point}' in result.decode()
    except subprocess.CalledProcessError as error:
        print(f'Error checking if device is mounted: {error}')
        raise

def mount_volume(device, mount_point):
    # Create the mount point directory
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)

    # Check if the device is already mounted
    if is_mounted(device, mount_point):
        print(f'{device} is already mounted on {mount_point}')
    else:
        # Mount the volume
        try:
            subprocess.check_call(['sudo', 'mount', device, mount_point])
            subprocess.check_call(['sudo', 'chown', f'{os.getenv("USER")}:{os.getenv("USER")}', mount_point])
            print(f'Volume mounted on {mount_point}')
        except subprocess.CalledProcessError as error:
            print(f'Error mounting volume: {error}')
            raise

def check_backup_data(mount_point):
    # List the contents of the mount point to verify backup data
    try:
        contents = os.listdir(mount_point)
        if contents:
            print('Backup data found:')
            for item in contents:
                print(item)
        else:
            print('No backup data found in the volume.')
    except OSError as error:
        print(f'Error accessing mount point: {error}')
        raise

# Example usage
device = '/dev/xvdf'  # Replace with your actual device name
mount_point = '/mnt/mybackup'

try:
    mount_volume(device, mount_point)
    check_backup_data(mount_point)
except Exception as e:
    print(f'Failed to verify backup data: {e}')
