# checkpoint_scrubbing_webservice
Simple web service to clean documents and other files (convert to pdf).

Before using this web service you have to configure your Checkpoint instance: 
https://supportcenter.checkpoint.com/supportcenter/portal?eventSubmit_doGoviewsolutiondetails=&solutionid=sk137032

Installation:

1. Install Python 3.*
2. Create a working directory:
  $ mkdir scrubbing && cd scrubbing
3. Copy app.py to the directory
4. Set up a virtual environment to use for our application:
  $ python3 -m venv venv
  $ source venv/bin/activate
5. Install required modules
  $ pip install Flask
  $ pip install requests
  
To confugure app edit file app.py:
1. ALLOWED_EXTENSIONS - type of files
2. URL - url to your CheckPoint API
3. PORT - port to run app


Run the app:
  $ python3 app.py

