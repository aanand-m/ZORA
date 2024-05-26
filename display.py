import boto3

def get_data():
    # Replace with your bucket name
    bucket_name = "sentiment-data-bucket"
    access_key = "AKIA3YHIEH3CFQUZSW5Q"
    secret_key = "Rwj1XRFGxZSMlVkzptDzRm+XnGy/T50hy1yiTZWh"

    # Create S3 client
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Print each object's key (filename)
    fileList = []
    print("FILES IN S3:")
    for obj in response.get('Contents', []):
        fileList.append(obj['Key'])
  
    return fileList
