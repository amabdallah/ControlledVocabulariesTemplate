# What is Ansible?

Ansible is an open-source automation engine that automates software provisioning, configuration management, and application deployment. 

Designed for multi-tier deployments since day one, Ansible models your IT infrastructure by describing how all of your systems inter-relate, rather than just managing one system at a time.

It uses no agents and no additional custom security infrastructure, so it's easy to deploy - and most importantly, it uses a very simple language (YAML, in the form of Ansible Playbooks) that allow you to describe your automation jobs in a way that approaches plain English.

To know more about Ansible visit: https://www.ansible.com/how-ansible-works

# What is Docker?

Docker is an open platform for developers and sysadmins to build, ship, and run distributed applications, whether on laptops, data center VMs, or the cloud. Docker can package an application and its dependencies in a virtual container that can run on any Linux server. This helps enable flexibility and portability on where the application can run. 

To know more about Docker visit: https://www.docker.com/what-docker

# Customize deployment

## Ansible Playbooks

This folder, which you are browsing now, is an Ansible Playbook. Playbooks are Ansible's configuration, deployment and orchestration language. They can describe a policy you want your remote systems to enforce, or a set of steps in a general IT process

Playbooks are expressed in YAML format and have a minimum of syntax, which intentionally tries to not be a programming language or script, but rather a model of a configuration or a process

To know more about Ansible Playbooks visit: http://docs.ansible.com/ansible/playbooks.html

## What's in this playbook?

### deploy.yml

Contains the step instructions to deploy the apps on a given host. You can change the configuration and steps on this file but you may need some knowledge about writing Ansible playbooks to make significative and successful changes on the deployment. The most simple change you can do on this file is to set the hosts on which the applications will be deployed changing the `hosts` variable. Please take a look at the file to know more

### vars.yml

Is a declaration of variables that may be customized and would be used during the deployment. It's important to note that this is the file you will edit when you want to customize credentials, paths and names. For a better understanding, I encourage you to open it and read the comments for each variable

### hosts

Is a configuration file where you set the public ip address of the hosts where the apps will be deployed and the authorized user for such action. You can add as many hosts as you need and group them to make simultaneous deployments

### Files

In this folder you will find configuration templates. These make references to the variables on the `vars.yml` file, the values on the templates are substituted during the deployment and then placed on the target paths for its respective applications.

#### dockerfile.j2 

Is the template to generate images and containers for the WaDE django application

#### nginx.j2

Is the virtualhost for the nginx webserver. It has a single section with the following layout:

```
server {
    listen       80;
    server_name  <sub-domain-wade-variable>;
    charset utf-8;

    location / {
        proxy_pass http://<wade-container-variable>:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

where

* <sub-domain-wade-variable> is the variable which references the sub domain names for the WaDE application
* <wade-container-variable> is the name of the container where the WaDE application is deployed

This variables must be also defined on the file `vars.yml`

e. g:

```
# vars.yml
...
wade_container: wade

wade_allowed_hosts: vocabularies.westernstateswater.org
...
```

```
# files/nginx.j2
server {
    listen       80;
    server_name  {{wade_allowed_hosts}};
    charset utf-8;

    location / {
        proxy_pass http://{{wade_container}}:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### settings_wade.j2

Is the django config file for the WaDE application, it has a dictionary of strings which values are substituted during deployment with the values assigned to the variables on the `vars.yml` file
