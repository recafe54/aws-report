import boto3
import csv
# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
rows = []
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
    # rows.append(bucket)
    print(bucket)

# print(bucket)
# print(bucket['CreationDate'])

# fieldnames = ['Name','CreationDate']

# with open('s3_listing.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(rows)

