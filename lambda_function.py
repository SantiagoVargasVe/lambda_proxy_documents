import boto3
import os

# Initialize AWS clients
ses = boto3.client('ses')
s3 = boto3.client('s3')

FROM_EMAIL = "documents@santiagovargas.co"
TO_EMAIL = "dianavegag@hotmail.com"  # Replace this

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Generate pre-signed URL (valid for 1 hour)
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3600  # 1 hour
        )

        subject = f"📥 New File Uploaded: {key}"
        body = f"""A new file has been uploaded to your bucket:

Bucket: {bucket}
File: {key}

Download it here (valid for 1 hour):
{url}
"""

        # Send email via SES
        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [TO_EMAIL]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )

    return {"statusCode": 200, "body": "Email sent with link."}
