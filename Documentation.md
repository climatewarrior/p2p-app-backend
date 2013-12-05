Installation Guide
=========
----------
Backend
----


-----------
Prerequisites
-------------
- You have an Amazon Web Services(AWS) account 
- Python and Flask are installed on the system
- The source code is stored in a Git repository


In order to run our application, you first need to set up a server. To ensure remote access, it might be a good choice to use some well-known cloud application platforms. For our application, we recommend using Amazon Elastic Cloud Computing (Amazon EC2). Here is the link that shows how to get started with Amazon EC2 Linux instances (Ubuntu): http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html

Once the Amazon EC2 instance is set up, the next step is to configure that instance. First, log in to the EC2 instance (usually done through an SSH connection) and type the following command:
```sh
sudo apt-get install python-pip
```
pip is a tool for installing and managing Python packages. <br /> Note: we are using Python 2.7

Then you need to install Flask. Type the following command:
```sh
sudo pip install Flask
```
Regarding the other dependencies, please refer to the following commands:
```sh
pip install Flask-BasicAuth
pip install Flask-PyMongo
...

```
Here we do not enumerate all the dependency installation commands. For complete dependencies, please check the source code p2p.py on the Github. 

Next, type the following command:


```sh
sudo apt-get install apache2 libapache2-mod-wsgi
```
This installs the web server Apache2 as well as a Python WSGI module.<br />
<br />
If you point yourself to your EC2 domain (either the DNS address you used to connect to your server via SSH or a URL you have pointed towards it), you will see a welcoming message from the Apache web server.
Type the following:
```sh
sudo mkdir /var/www
cd /var/www
sudo git clone git@github.com:climatewarrior/p2p-app-backend.git
cd ./p2p-app-backend
sudo nano p2p.wsgi
```
The .wsgi file should match the name of the Python file containing the "yourflaskapp = Flask(__name__)" line. Make sure that in this file (the main python file, not your newly-created .wsgi file), you have any yourflaskapp.run() calls contained within the "if __name__ == '__main__':" clause. Otherwise, your app will be starting a local WSGI server instead of forwarding it through mod_wsgi and Apache.

The p2p.wsgi file is simple and should look like the following:

```sh
import sys
sys.path.insert(0, '/var/www/p2p-app-backend')

from p2p import app as application

```

Now, type the following commands:
```sh
cd /etc/apache2/sites-available/
sudo nano sitename.conf

```
Note: sitename should be the DNS address of the EC2 instance(For example, ec2-54-xxx-xxx-xxx.us-west-2.compute.amazonaws.com). The content of this file should look like this:
```sh
<VirtualHost *:80>
         WSGIDaemonProcess p2p
         WSGIPassAuthorization On
     WSGIScriptAlias / /var/www/p2p-app-backend/p2p.wsgi

     <Directory /var/www/p2p-app-backend>
            WSGIProcessGroup p2p
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
     </Directory>
</VirtualHost>


```
Then all that is left to do is disable the Apache default page and enable the Flask application:
```sh
sudo a2dissite default
sudo a2ensite sitename.conf
sudo /etc/init.d/apache2 restart


```
Now if you navigate to your page, you should see your Flask application up and running. 


Install MongoDB
----------------
For our application, we are using MongoDB as the database. Here is the installation instruction.

The MongoDB downloads repository provides the mongodb-10gen package, which contains the latest stable release. Additionally you can install previous releases of MongoDB.

You cannot install this package concurrently with the mongodb, mongodb-server, or mongodb-clients packages provided by Ubuntu.

The Ubuntu package management tool (i.e. dpkg and apt) ensure package consistency and authenticity by requiring that distributors sign packages with GPG keys. Issue the following command to import the MongoDB public GPG Key:
```sh
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10


```
Create a /etc/apt/sources.list.d/mongodb.list file using the following command.
```sh
sudo apt-get update


```

Issue the following command to install the latest stable version of MongoDB:
```sh
sudo apt-get install mongodb-10gen

```

When this command completes, you have successfully installed MongoDB.



