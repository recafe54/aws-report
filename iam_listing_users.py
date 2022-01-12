import boto3
import csv

client=boto3.client('iam')
users = client.list_users()
service_ = 's3'
rows = []
for user in users['Users']:
    temp_row = dict()
    isGroup = False
    isManagedPolicy = False
    isInlinePolicy = False

    print(user['UserName'])
    temp_row['Name']= user['UserName']
    temp_row['Policies_from_Groups'] = []
    temp_row['Managed_Policies'] = []
    temp_row['Inline_Policies'] = []

    List_of_Groups =  client.list_groups_for_user(UserName=user['UserName'])
    if len(List_of_Groups['Groups']) > 0:
        for group in List_of_Groups['Groups']:
            if service_ in group['GroupName'].lower():
                print(f'\n {service_}-related-IAM-Groups:')
                print(group['GroupName'])
                # temp_row['GroupName']
                isGroup = True
                response = client.list_attached_group_policies(GroupName=group['GroupName'])
                print(response['AttachedPolicies'])
                for policy_ in response['AttachedPolicies']:
                    temp_row['Policies_from_Groups'].append(policy_['PolicyName'])
                # get_policy_group = client.get_policy(PolicyArn=group['Arn'])
                # print(get_policy_group['Policy']['PolicyName'])
            else:
                # print('None')
                pass

    managed_user_policies =  client.list_attached_user_policies(UserName=user['UserName'])
    
    if len(managed_user_policies['AttachedPolicies']) > 0:
        for managed_policy in managed_user_policies['AttachedPolicies']:
            policy_name = managed_policy['PolicyName']
            if service_ in policy_name.lower():
                print(f'\n {service_}-related-IAM-managed-Policies attached directly:')
                print(policy_name)
                print(managed_policy)
                isManagedPolicy = True
                temp_row['Managed_Policies'].append(managed_policy['PolicyName'])
            else:
                # print('None')
                pass
    

    inline_user_policies =  client.list_user_policies(UserName=user['UserName'])
    
    if len(inline_user_policies['PolicyNames']) > 0:
        for inline_policy in inline_user_policies['PolicyNames']:
            if service_ in inline_policy.lower():
                print(f'\n {service_}-related-IAM-inline-Policies attached directly:')
                print(inline_policy)
                isInlinePolicy = True
                temp_row['Inline_Policies'].append(inline_policy)
            else:
                # print('None')
                pass
    
    print('-------- \n')
    if isGroup or isManagedPolicy or isInlinePolicy:
        rows.append(temp_row)


# managed_user_policies =  client.list_attached_user_policies(UserName='hieunp1')

# inline_user_policies =  client.list_user_policies(UserName='hieunp1')


# print(inline_user_policies['PolicyNames'])
# print(len(managed_user_policies['AttachedPolicies']))

# print()

fieldnames = ['Name','Policies_from_Groups','Managed_Policies','Inline_Policies']

with open('iam_listing_users.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
