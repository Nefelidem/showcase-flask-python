
# Web IDV Demo in Python using Flask

## Introduction

This project demonstrates the integration of Authenteq Web IDV with the application written in Python.
It's implemented with Flask and jinja2 for the details page. 


## Running project
python version 3.7 or higher is required


The current project is implemented with python version 3.8

###Flask configuration from environment variables
##### Use environment variables directly in your code.

Linux
```
export CLIENT_ID=<your client id>
export CLIENT_SECRET=<your client secret>
```
Windows
```
set CLIENT_ID=<your client id>
set CLIENT_SECRET=<your client secret>
```

You can find these values in the [Customer Dashboard](https://customer-dashboard.app.authenteq.com/customer/api-keys).

To run this application using Flask set the following environmental variables:
Linux
```
export FLASK_APP=main_application.py 
export FLASK_ENV=development
```

Windows
```
set FLASK_APP=main_app.py 
set FLASK_ENV=development
```

Run:
```
flask run
```


The frontend starts on port 5000 on the localhost.

Open [https://localhost:5000](https://localhost:5000).

The application contains:
* index  (/) - home page with Button which will initiate the verification process
* results (/results) displays the results of the verification



