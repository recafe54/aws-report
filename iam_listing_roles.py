import boto3
import csv

client=boto3.client('iam')
roles = client.list_roles()
service_ = 's3'
rows = []

for role in roles['Roles']:
    temp_row = dict()

    print(role['RoleName'])

    isGroup = False
    isManagedPolicy = False
    isInlinePolicy = False

    temp_row['Role_Name']= role['RoleName']
    temp_row['Managed_Policies'] = []
    temp_row['Inline_Policies'] = []

    managed_role_policies =  client.list_attached_role_policies(RoleName=role['RoleName'])
    
    if len(managed_role_policies['AttachedPolicies']) > 0:
        for managed_policy in managed_role_policies['AttachedPolicies']:
            policy_name = managed_policy['PolicyName']
            if service_ in policy_name.lower():
                print(f'\n {service_}-related-IAM-managed-Policies attached directly:')
                print(policy_name)


                isManagedPolicy = True
                temp_row['Managed_Policies'].append(policy_name)
                # CAN'T GET MORE INFOR ABOUT POLICIES
                # if policy_name == 'Amazon'+service_.upper()+'FullAccess': #AmazonS3FullAccess
                #     print(managed_policy)
                # else:
                #     response = client.get_policy(PolicyArn=managed_policy['PolicyArn'])
                #     print(response)
            else:
                # print('None')
                pass
    

    inline_role_policies =  client.list_role_policies(RoleName=role['RoleName'])
    
    if len(inline_role_policies['PolicyNames']) > 0:
        for inline_policy in inline_role_policies['PolicyNames']:
            if service_ in inline_policy.lower():
                print(f'\n {service_}-related-IAM-inline-Policies attached directly:')
                print(inline_policy)

                isInlinePolicy = True
                temp_row['Inline_Policies'].append(inline_policy)
            else:
                # print('None')
                pass
    
    if isInlinePolicy or isManagedPolicy:
        rows.append(temp_row)
    
    
    print('-------- \n')



fieldnames = ['Role_Name','Managed_Policies','Inline_Policies']

with open('iam_listing_roles.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)