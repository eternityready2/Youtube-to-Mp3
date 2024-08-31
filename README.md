Welcome to Eternity Ready. This repo is a new app we created in August 2024. Made in python using the Stream Lit, an open source framework. This app has a front-end UI - web page @ https://yt.eternityready.com
The script allows users to download Videos and MP3 Audio from YouTube. The script allows videos and MP3 Audio files to be downloaded - saved to the web host (where this script is installed) or to the user's device.

This script requires a VPS / Dedicated Server with root and command line access. You have to install Stream Lit and Python. 

>>> The following is instructions on how to setup the app and the server:

\\ Introduction:

This guide provides a step-by-step process to deploy a Streamlit application on a Linux server.

Prerequisites

● Linux server with root access.

Step 1: Update the Server

1. Update and Upgrade Packages
   
Open the terminal and run the following commands to ensure your server packages are
up-to-date:

sudo apt update && sudo apt upgrade

Step 2: Install Python and pip

3. Install Python 3 and pip by running:
 
sudo apt install python3 python3-pip

Step 3: Install Streamlit

6. With Python installed, install Streamlit by running:

pip3 install streamlit

Step 4: Deploy Your Streamlit App

9. Use the cd command to navigate to the directory where your Streamlit app is located:
    
cd /path/to/your/app

11. Start the Streamlit app by running:
    
streamlit run your_app.py

Step 5: Set Up a Systemd Service

13. To keep your Streamlit app running in the background and ensure it restarts
automatically, create a systemd service.

15. Create a Service File. Open a new service file with the following command:
    
sudo nano /etc/systemd/system/streamlit-app.service

17. Add Service Configuration. Copy and paste the following content into the service file.
    
[Unit]

Description=Streamlit App
After=network.target

[Service]

User=your_username

WorkingDirectory=/path/to/your/app

ExecStart=/usr/bin/python3 -m streamlit run your_app.py

Restart=always

[Install]

WantedBy=multi-user.target

19. Start and Enable the Service
    
sudo systemctl start streamlit-app

21. Enable the service to start on boot:
    
sudo systemctl enable streamlit-app

Step 7: Access Your Streamlit App

Once everything is set up, you can access your Streamlit app by navigating to your
server's IP address or domain name in a web browser.


>>> Commands for the Stream LIT app 

1. Restart the app
   
systemctl restart streamlit-app.service

2. Start the app

systemctl start streamlit-app.service

3. Check the status of the app

systemctl status streamlit-app.service 
