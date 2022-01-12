import boto3

# Retrieve a bucket's ACL
s3 = boto3.client('s3')

result = s3.get_bucket_acl(Bucket="haphamd-test-pipelines")
print(result)