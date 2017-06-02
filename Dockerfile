FROM ubuntu:latest

# Add the add-repository command 
RUN apt-get update && apt-get -y install \
	software-properties-common \
	python-software-properties

# Add Ansible Repo
RUN apt-add-repository -y ppa:ansible/ansible

RUN apt-get update && apt-get -y \
	install \
	python \
	python-pip \
	ansible \
	libffi-dev \
	libxml2-dev \
	libxslt1-dev \
	lib32z1-dev \
	libssl-dev \
	git \
	zlib1g-dev \
    libxslt-dev \
    python-dev \
	iputils-ping \
	telnet \
	vim \
	wget

# Misc Ansible and Cisco dependancies
RUN pip install \
	pyntc \
	napalm \
	ntc-ansible \
	jinja2 \
	lxml \
	terminal
   

# Get the Ansible pre 2.3 Cisco Spark Module
RUN wget https://raw.githubusercontent.com/drew-russell/ansible/610dc9993cbcd15bf7e5e7771090debb55f1ec76/lib/ansible/modules/notification/cisco_spark.py  -O /usr/lib/python2.7/dist-packages/ansible/modules/extras/notification/cisco_spark.py

RUN echo "[local]" >> /etc/ansible/hosts && \
    echo "localhost" >> /etc/ansible/hosts

# Expose the default port
# EXPOSE 2222:22

#ENV ANSIBLE_GATHERING smart
ENV ANSIBLE_HOST_KEY_CHECKING false
ENV ANSIBLE_RETRY_FILES_ENABLED false
#ENV ANSIBLE_ROLES_PATH /ansible/playbooks/roles
#ENV ANSIBLE_SSH_PIPELINING True
#ENV PATH /ansible/bin:$PATH
#ENV PYTHONPATH /ansible/lib

RUN rm -rf /ansible
RUN mkdir /root/.ssh
RUN echo "" >> /root/.ssh/known_hosts
RUN export PYTHONPATH="${PYTHONPATH}:/ansible"
RUN pip install pydot
RUN pip install --upgrade pip
# Had to seperate this after the fact to get the paths and all working - run graphviz seperately
RUN apt-get -y install graphviz

RUN echo "version 0.2"

WORKDIR /ansible

RUN pip install git+git://github.com/jasonbarbee/mnet.git
RUN git clone https://github.com/jasonbarbee/mnet /mnet

# Clone Ansible Cisco Inventory Tooling
RUN git clone https://github.com/jasonbarbee/ansible-cisco-inventory.git /ansible


# Clone NTC Ansible to shared library
RUN git clone https://github.com/networktocode/ntc-ansible --recursive /usr/share/ansible/ntc-ansible

# Fix some NTC setup files conflicting with Ansible Namespace.
RUN mv /usr/share/ansible/ntc-ansible/setup.py /usr/share/ansible/ntc-ansible/oldsetup.py 
RUN mv /usr/share/ansible/ntc-ansible/setup.cfg /usr/share/ansible/ntc-ansible/oldsetup.cfg 
RUN mv /usr/share/ansible/ntc-ansible/ntc-templates/setup.py /usr/share/ansible/ntc-ansible/ntc-templates/oldsetup.py


# Copy NTC into Inventory tooling folder
RUN cp /usr/share/ansible/ntc-ansible/* -r /ansible/


RUN cp /ansible/ansible.cfg /etc/ansible

RUN pip install --upgrade paramiko