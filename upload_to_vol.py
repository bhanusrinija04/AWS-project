"""
Your module description
"""
import shutil

source_file_path = '/home/ec2-user/environment/example.txt'
destination_path = '/mnt/myebs/file'

shutil.copy2(source_file_path, destination_path)

print(f'File copied to {destination_path}')
