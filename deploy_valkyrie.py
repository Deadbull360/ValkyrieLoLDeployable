import boto3, os
from zipfile import ZipFile
from io import BytesIO

# Create zip file of the files to be deployed
print('Creating zip')

zip_stream = BytesIO()
zip = ZipFile(zip_stream, mode='w')
for root, dirs, files in os.walk('Deployable'):
    zip.write(root)
    for filename in files:
        zip.write(os.path.join(root, filename))
zip.close()
zip_stream.seek(0)
zip_bytes = zip_stream.read()

# Create s3 client
print('Creating S3 client')
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws-access-key'],
    aws_secret_access_key=os.environ['aws-secret-access-key']
)

print('Uploading zip')
s3.upload_fileobj(zip_bytes, os.environ['aws-deploy-bucket'], 'latest.zip')