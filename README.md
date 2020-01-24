# CiscoLiveSDWAN
Cisco Live SDWAN Development and Scripting - LABCRS-2000 Lab Reset Script

This script should be run in a Python v3 environment - ensure that all dependiecies are installed or upgraded. You must ensure that you are connected to the correct VPN environment for access to the correct vManage.

This script relies on two JSON files that contain the reset config for BR2-VEDGE and BR1-VEDGE1. Ensure that the JSON files BR2_Template_V01.json and BR1_1_Template_V01.json are in the same directory as benscript.py

To run the program, change to the directory with the script and files (cd dir)

> python3 benscript.py
(No input is needed)

IF you receive an Status 400, please ensure that the templates have been attached to the correct devices.

IF you receive an output " - does not exist or is misnamed. Please manually inspect the traffic policy" or " - Please manually inspect the central policy", please visually inspect the policies and delete any user created policies.
