import boto3
import os

# Get parameters (will throw exception if unset)
old_cidr = os.environ["OLD_CIDR"]
new_cidr = os.environ["NEW_CIDR"]

# Create an initial client in the default region
client = boto3.client('ec2', 'us-east-1')

# Get a list of regions
result = client.describe_regions()

# Check each region
regions = result["Regions"]
for region in regions:

  region_name = region["RegionName"]
  print(region_name)

  ec2c = boto3.client('ec2', region_name)
  ec2 = boto3.resource('ec2', region_name)
  result = ec2c.describe_security_groups()

  # Check each security group
  security_groups = result["SecurityGroups"]
  for security_group in security_groups:

    # Check each security group rule
    ip_permissions = security_group["IpPermissions"]
    for ip_permission in ip_permissions:

      # Check each IP range
      ip_ranges = ip_permission["IpRanges"]
      for ip_range in ip_ranges:

        cidr_ip = ip_range["CidrIp"]

        # Does the rule contain a reference to the old CIDR?
        if cidr_ip == old_cidr:
          print("  [UPDATE   ] " + security_group["GroupId"] + " " + security_group["GroupName"])

          # Revoke rule for old CIDR and add rule for new one
          sgc = ec2.SecurityGroup(security_group["GroupId"])
          sgc.revoke_ingress(IpProtocol=ip_permission["IpProtocol"], CidrIp=old_cidr, FromPort=ip_permission["FromPort"], ToPort=ip_permission["ToPort"])
          sgc.authorize_ingress(IpProtocol=ip_permission["IpProtocol"], CidrIp=new_cidr, FromPort=ip_permission["FromPort"], ToPort=ip_permission["ToPort"])

        # Does the rule contain a reference to the new CIDR?
        if cidr_ip == new_cidr:
          print("  [NO CHANGE] " + security_group["GroupId"] + " " + security_group["GroupName"])
