# Ansible Cisco Inventory
For onboarding a network to Cisco My Devices or Cisco TotalCare FAST and EASY.
For people who don't have time to install a collector, discover subnets, deal with SNMP issues, etc.

## Goal: Help Make Cisco Inventories easier and automated.

## Why use this?
1. You onboard the device once in bulk. No SNMP or discovery guess work.
2. Automation value add - Now that device can be automated by Ansible for other things.
3. No data leaves the network other than the CSV.
4. Easy EOX reports and contract renewal quoting for customers.
5. Easy IOS version reports for customer.
6. Walk away with a Cisco integrated deliverable they can access, and you can come back and run the scan any time.


## Prep work - you need Ansible and NTC-Ansible
1. Install Ansible
http://docs.ansible.com/ansible/intro_installation.html

2. Install NTC-Ansible into the working folder with this playbook.
https://github.com/networktocode/ntc-ansible

    * Option 1 usually works best.
One simple way to fix Ansible paths for this to work is to create a new folder for this repo, then clone this repo into it.
```git clone https://github.com/networktocode/ntc-ansible --recursive```

Example that will work every time
```
$ git clone https://github.com/networktocode/ntc-ansible.git --recursive
$ cd ntc-ansible
```
Clone/Unzip my repo inside ntc-ansible

Test your NTC Code library paths. If it does not work, my script will not work. 
If you get a working Help Document from this command you are good to go.
```
$ ansible-doc ntc_file_copy
```

Install NTC-Ansible Depedencies
```
pip install ntc-ansible
sudo apt-get install zlib1g-dev libxml2-dev libxslt-dev python-dev
pip install terminal
```

# Now to the Network Scanner
This does not use SNMP. It is a CLI parsing tool. So as long as we can login, we are good.
These modules **require SSH**. If you need telnet there is a way to make that happen. Open an issue if needed and I'll document it. Or the next time I need telnet I will document it.

Getting Started:
1. Make sure our ansible.cfg is within ntc-ansible folder. It forces the library folder.
2. Onboard devices with Ansible inventory file
Example
```yaml
[routers]
192.168.1.1

[routers:vars]
username='username'
password='password'
port=22
```
3. Scan the network
```bash
$ ansible-playbook -i inventory.yml cisco-mydevices.yml
```
4. You will get a file - *mydevices.csv*. This file can be dragged and uploaded straight to Cisco My Devices Tool.

https://cway.cisco.com/mydevices/

Don't worry about duplicates, or all the module serial numbers. It will be helpful in the reports.
* Choose Add New Devices and Import using the CSV Template option.

* Now you can run EOX reports on any Device or module in the entire scan!
* You can also share your Device Information with up to 15 other people for smartnet quoting or rough inventory review.

## See all your Inventory, modules, Site Address, and Contract info.
![](screenshots/Device-View-Cleaned.png)

## See EOX Reports for your Cisco Network
![](screenshots/EOL-Report-Cleaned.png)


## See your Contracts at a glance.
![](screenshots/Contract-Renewal-Cleaned.png)

# Onboarding to Totalcare
Select all the devices and click Download in SNTC 3.x Format.
Now you can import this file to Totalcare.

TODO: Possibly discuss all the steps to onboard a customer to Totalcare.

### License
MIT - Jason Barbee 2017
