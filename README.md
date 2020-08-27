
# Web IDV Demo in Python using Flask

## Introduction

This project demonstrates the integration of Authenteq Web IDV with the application written in Python.
It's implemented with Flask and jinja2 for the details page. 


## Running project

To run the project install first the following packages
```
Flask   
requests
python-dotenv 
flask_caching
secrets
flask_session
jinja2
```
The current project is implemented with python version 3.8

Create .env file with two variables:
```
CLIENT_ID=o7...My
CLIENT_SECRET=1D...M5
```

You can find these values in the [Customer Dashboard](https://customer-dashboard.app.authenteq.com/customer/api-keys).

To run this application from command line:
Navigate to the project folder and type 
```
 python retrieve_results_file.py
```

The frontend starts on port 5000 on the localhost.

Open [https://localhost:5000](https://localhost:5000).

The application contains three flask routes:
* index  (/) - initiates the process,
* results (/results) which calls the verification process in the home page
* verification details  (/details) - displays the results from the verification process


