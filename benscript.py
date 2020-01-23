#####################################################################
#Cisco SDWAN Lab CRS2000 Reset Script                               #
#Date: June 2019 Edited: Jan 2020                                   #
#Author: Ben Sealy (bsealy@cisco.com)                               #
#####################################################################
import requests
from requests.packages import urllib3
import json
#import urllib3
import re
import os
import time
import pprint
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print ('Sit Back - Enjoy the Ride - This will take about 1 minute to complete')
##################################################################################################################################
#Connection Information for SDWAN 2000 dCloud Environment
##################################################################################################################################
vmanage_ip = '198.18.1.10:8443'
vmanage_pw = 'cisco.123'
request_url = '/j_security_check'
sess = requests.session()
r = sess.post('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
##################################################################################################################################
#Determine input values using student number
##################################################################################################################################
BR2_EDGE_uuid = ''
BR2_VEDGE_name = ('BR2-VEDGE')
BR1_VEDGE1_uuid = ''
BR1_VEDGE1_name = ('BR1-VEDGE1')
Centralized_Policy_name = ('Centralized-Policy')
VPN40_IPSEC_DATA = ('VPN40-IPSEC-DATA')
VPN10_Service_Insertion = ('VPN10-Service-Insertion')
VPN20_Hub_Spoke = ('VPN20-Hub-Spoke')
BR1_NAT_Policy = ('BR1-NAT-Policy')
##################################################################################################################################
#Device templates
##################################################################################################################################
BR2_VEDGE_template = ('vEdge_Single_Router_Branch_Guest_IPSec_V01')
    #BR2_VEDGE_deleted_template = ('vEdge_Single_Router_Branch_Guest_IPSec_V02')
BR2_VEDGE_BGP_template = ('vEdge_Single_Router_Branch_Guest_IPSec_BGP_Peer')
BR1_VEDGE1_template = ('vEdge_Dual_Router_V01')
BR1_VEDGE1_NAT_template = ('vEdge_Dual_Router_Service_Side_NAT')
##################################################################################################################################
#Retrieve UUIDs for vedges
##################################################################################################################################
request_url = '/dataservice/system/device/vedges?model=vedge-cloud&&&&validity=valid'
r = requests.get('https://' + vmanage_ip + request_url, verify=False, auth=('admin','cisco.123'))
data = r.json()['data']
try:
    BR2_VEDGE_uuid = next(
        (entry for entry in data
            if 'host-name' in entry
            and entry['host-name'] == BR2_VEDGE_name
        )
    )['uuid']
    BR1_VEDGE1_uuid = next(
        (entry for entry in data
            if 'host-name' in entry
            and entry['host-name'] == BR1_VEDGE1_name
        )
    )['uuid']
except StopIteration:
    pass
##################################################################################################################################
##################################################################################################################################
print ('Device UUID tasks done, processing for 2 seconds')
for remaining in range(2, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
#Get list of device templates
##################################################################################################################################
request_url = '/dataservice/template/device/'
r = sess.get('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
template_list_json = r.json()
template_list = template_list_json['data']
##################################################################################################################################
#Get list of feature templates
##################################################################################################################################
request_url = '/dataservice/template/feature/'
r = sess.get('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
feature_list_json = r.json()
feature_list = feature_list_json['data']
##################################################################################################################################
#Get list of local policies
##################################################################################################################################
request_url = '/dataservice/template/policy/vedge'
r = sess.get('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
policy_list_json = r.json()
policy_list = policy_list_json['data']
##################################################################################################################################
#Get list of central policies
##################################################################################################################################
request_url = '/dataservice/template/policy/vsmart'
r = sess.get('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
centpolicy_list_json = r.json()
centpolicy_list = centpolicy_list_json['data']
##################################################################################################################################
#Get list of policy control definitions
##################################################################################################################################
request_url = '/dataservice/template/policy/definition/control'
r = sess.get('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
controlpolicy_list_json = r.json()
controlpolicy_list = controlpolicy_list_json['data']
##################################################################################################################################
#Get list of policy data definitions
##################################################################################################################################
request_url = '/dataservice/template/policy/definition/data'
r = sess.get('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
datapolicy_list_json = r.json()
datapolicy_list = datapolicy_list_json['data']

print ('Get Lists tasks done, processing for 2 seconds')
for remaining in range(2, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
#########################################################################################################################
#########################################################################################################################
#set temp id to false, empty
##################################################################################################################################
BR2_VEDGE_templateId = "False"
Centralized_Policy_policyId = "False"
Test_Policy_policyId = "False"
Control_VPN20_defId = "False"
Control_VPN10_defId = "False"
Data_VPN40_defId = "False"
Data_BR1_defId = "False"
BR2_VEDGE_deleted_templateId = "False"
BR2_VEDGE_BGP_templateId = "False"
BR1_VEDGE1_templateId = "False"
BR1_VEDGE1_NAT_templateId = "False"
##################################################################################################################################
#set/get template ID
##################################################################################################################################
for idx, val in enumerate(template_list):
    if val['templateName'] == BR2_VEDGE_template:
        BR2_VEDGE_templateId = val['templateId']
# for idx, val in enumerate(template_list):
#     if val['templateName'] == BR2_VEDGE_deleted_template:
#         BR2_VEDGE_deleted_templateId = val['templateId']
for idx, val in enumerate(template_list):
    if val['templateName'] == BR2_VEDGE_BGP_template:
        BR2_VEDGE_BGP_templateId = val['templateId']
for idx, val in enumerate(template_list):
    if val['templateName'] == BR1_VEDGE1_template:
        BR1_VEDGE1_templateId = val['templateId']
for idx, val in enumerate(template_list):
    if val['templateName'] == BR1_VEDGE1_NAT_template:
        BR1_VEDGE1_NAT_templateId = val['templateId']
##################################################################################################################################
#set/get policy ID
##################################################################################################################################
for idx, val in enumerate(centpolicy_list):
    if val['policyName'] == Centralized_Policy_name:
        Centralized_Policy_policyId = val['policyId']
##################################################################################################################################
#set/get def ID
###################################################################################################################################
for idx, val in enumerate(controlpolicy_list):
    if val['name'] == VPN20_Hub_Spoke:
       Control_VPN20_defId = val['definitionId']
for idx, val in enumerate(controlpolicy_list):
    if val['name'] == VPN10_Service_Insertion:
       Control_VPN10_defId = val['definitionId']
for idx, val in enumerate(datapolicy_list):
    if val['name'] == VPN40_IPSEC_DATA:
       Data_VPN40_defId = val['definitionId']
for idx, val in enumerate(datapolicy_list):
    if val['name'] == BR1_NAT_Policy:
       Data_BR1_defId = val['definitionId']
##################################################################################################################################
print ('Indexing tasks done, processing for 2 seconds')
for remaining in range(2, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
#Reattach V01 Device Template to Br2 Template
    #Get list of device template objects
##################################################################################################################################
headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache', 'accept': '*/*', 'accept-encoding': 'gzip, deflate'}
request_url = '/dataservice/template/device/config/attachfeature/'
body = json.loads(open('./BR2_Template_V01.json').read().replace("$BR2_VEDGE_templateId", BR2_VEDGE_templateId).replace("$BR2_VEDGE_uuid", BR2_VEDGE_uuid))
r = sess.post('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw,), json=body, headers=headers)
if r.status_code is 200:
    print (BR2_VEDGE_template + ' has been attached to ' + BR2_VEDGE_name)
else:
    print (r.status_code)
    print ('Template failed to attach to ' + BR2_VEDGE_name)

print ('BRANCH2 Template Attach done, processing for 10 seconds')
for remaining in range(10, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
#Reattach V01 Device Template to Br1-vedge1 Template
    #Get list of device template objects
##################################################################################################################################
headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache', 'accept': '*/*', 'accept-encoding': 'gzip, deflate'}
request_url = '/dataservice/template/device/config/attachfeature/'
body = json.loads(open('./BR1_1_Template_V01.json').read().replace("$BR1_VEDGE1_templateId", BR1_VEDGE1_templateId).replace("$BR1_VEDGE1_uuid", BR1_VEDGE1_uuid))
r = sess.post('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw,), json=body, headers=headers)
if r.status_code is 200:
    print (BR1_VEDGE1_template + ' has been attached to ' + BR1_VEDGE1_name)
else:
    print (r.status_code)
    print ('Template failed to attach to ' + BR1_VEDGE1_name)

print ('BRANCH1 VEDGE1 Template Attach done, processing for 10 seconds')
for remaining in range(10, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
#Delete Templates
##################################################################################################################################
# if BR2_VEDGE_templateId is "False":
#     print BR2_VEDGE_deleted_template + ' does not exist or is misnamed. Please manually inspect the Device Templates'
# else:
#     request_url = '/dataservice/template/device/' + BR2_VEDGE_deleted_templateId
#     r = sess.delete('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
#     if r.status_code is 200:
#         print (BR2_VEDGE_deleted_template + ' has been deleted.')
#     else:
#         print r.status_code
#         print 'Failed to delete ' + BR2_VEDGE_deleted_template
##################################################################################################################################
#Deactivate
##################################################################################################################################
if Centralized_Policy_policyId is "False":
    print (Centralized_Policy_name + ' does not exist or is misnamed. Please manually inspect the central policy')
else:
    request_url = '/dataservice/template/policy/vsmart/deactivate/' + Centralized_Policy_policyId + '?confirm=true'
    r = sess.post('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
    if r.status_code is 200:
        print (Centralized_Policy_name + ' has been deactivated.')
    else:
        print (r.status_code)
        print ('Failed to deactivate ' + Centralized_Policy_name)

print ('Centralized Policy deactivation done, processing for 30 seconds')
for remaining in range(30, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
#Delete Policy
##################################################################################################################################
if Centralized_Policy_policyId is "False":
    print (Centralized_Policy_name + ' does not exist or is misnamed. Please manually inspect the central policy')
else:
    print (Centralized_Policy_policyId)
    request_url = '/dataservice/template/policy/vsmart/' + Centralized_Policy_policyId
    r = sess.delete('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
    if r.status_code is 200:
        print (Centralized_Policy_name + ' has been deleted.')
    else:
        print (r.status_code)
        print ('Failed to delete ' + Centralized_Policy_name)

print ('Centralized Policy deletion done, processing for 10 seconds')
for remaining in range(10, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
#Delete control and data policy definitions
##################################################################################################################################
if Control_VPN20_defId is "False":
    print (VPN20_Hub_Spoke + ' does not exist or is misnamed. Please manually inspect the traffic policy')
else:
    print (Control_VPN20_defId)
    request_url = '/dataservice/template/policy/definition/control/' + Control_VPN20_defId
    r = sess.delete('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
    if r.status_code is 200:
        print (VPN20_Hub_Spoke + ' has been deleted.')
    else:
        print (r.status_code)
        print ('Failed to delete ' + VPN20_Hub_Spoke)
##################################################################################################################################
print ('VPN20 Policy deletion done, processing for 2 seconds')
for remaining in range(2, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
if Control_VPN10_defId is "False":
    print (VPN10_Service_Insertion + ' does not exist or is misnamed. Please manually inspect the traffic policy')
else:
    print (Control_VPN10_defId)
    request_url = '/dataservice/template/policy/definition/control/' + Control_VPN10_defId
    r = sess.delete('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
    if r.status_code is 200:
        print (VPN10_Service_Insertion + ' has been deleted.')
    else:
        print (r.status_code)
        print ('Failed to delete ' + VPN10_Service_Insertion)
##################################################################################################################################
print ('VPN10 Policy deletion done, processing for 2 seconds')
for remaining in range(2, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
if Data_VPN40_defId is "False":
    print (VPN40_IPSEC_DATA + ' does not exist or is misnamed. Please manually inspect the traffic policy')
else:
    print (Data_VPN40_defId)
    request_url = '/dataservice/template/policy/definition/data/' + Data_VPN40_defId
    r = sess.delete('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
    if r.status_code is 200:
        print (VPN40_IPSEC_DATA + ' has been deleted.')
    else:
        print (r.status_code)
        print ('Failed to delete ' + VPN40_IPSEC_DATA)
##################################################################################################################################
print ('VPN40 Policy deletion done, processing for 2 seconds')
for remaining in range(2, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
##################################################################################################################################
if Data_BR1_defId is "False":
    print (BR1_NAT_Policy + ' does not exist or is misnamed. Please manually inspect the traffic policy')
else:
    print (Data_BR1_defId)
    request_url = '/dataservice/template/policy/definition/data/' + Data_BR1_defId
    r = sess.delete('https://' + vmanage_ip + request_url, verify=False, auth=('admin',vmanage_pw))
    if r.status_code is 200:
        print (BR1_NAT_Policy + ' has been deleted.')
    else:
        print (r.status_code)
        print ('Failed to delete ' + BR1_NAT_Policy)
##################################################################################################################################
print ('VPN40 Policy deletion done, processing for 2 seconds')
for remaining in range(2, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")
##################################################################################################################################
print ('SCRIPT EOF')
