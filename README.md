# Financial Regulations Dictionary

Financial Regulations Dictionary (FRD) is a platform that aims to help compliance officers to better manage all the financial regulations that matter them in practical and efficient manner. The platform provides a set of tools that allow the user to monitor, capture and search through new regulatory updates.

## Installation

Follow these step-by-step instructions to run FRD on your machine.

### Step 1
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [virtualenv](https://virtualenv.pypa.io/en/latest/).

To get [pip](https://pip.pypa.io/en/stable/), run the following command in your terminal
```bash
easy_install pip
```

After [pip](https://pip.pypa.io/en/stable/) is installed successfully, run the following commance to install [virtualenv](https://virtualenv.pypa.io/en/latest/)
```bash
pip install virtualenv
```

### Step 2
After installing [virtualenv](https://virtualenv.pypa.io/en/latest/) as instructed, navigate to your local FRD directory via terminal
```bash
cd path/to/FRD
```

Then run the following command to create a new virtual enviroment,
```bash
virtualenv env
```
and then activate the virtual enviroment by running the following command
```bash
source env/bin/activate
```

Now you should see (env) before your prompt, (env)$, which indicates that you’re running within the ‘env’ virtualenv.

### Step 3
Run the following command to install all of FRD's dependencies
```bash
pip install -r requirements.txt
```

Wait for the installations to finish and then move to the next step


### Step 4
After successfully installing all the dependencies as instructed, before you run FRD, make sure you are in the parent directory which contains the manage.py file. This should be right under the parent directory along with the README.md and requirements.txt files.

To start FRD, run the following command
```bash
python manage.py runserver
```

You should see something like this

```bash
Performing system checks...

System check identified some issues:

WARNINGS:
?: (urls.W001) Your URL pattern '^$' uses include with a route ending with a '$'. Remove the dollar from the route to avoid problems including URLs.

System check identified 1 issue (0 silenced).
April 24, 2019 - 01:58:27
Django version 2.0, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
[24/Apr/2019 01:58:28] "GET / HTTP/1.1" 200 4977
```

Now, using your preferred browser, go to http://127.0.0.1:8000/

## Testing
For testing FRD without registering a new user, please use the following credentials:

### Test User 1
Username: admin<br />
Password: frdtestpass

### Test User 2
Username: ioanna_mesimeri<br />
Password: frdtestpass2


## Author
Name: Mario Tawfelis<br />
Degree: BEng Computer Systems Engineering with Industrial Experience<br />
University: Queen Mary University of London<br />
Personal email: mario.tawfelis@outlook.com<br />
Academic email: m.sobhy@se15.qmul.ac.uk<br />
Student ID: 150612793





