# Web IDV Demo in Python using Flask

## Introduction

This project demonstrates the integration of Authenteq Web IDV with the application written in Python.
It's implemented with Flask and jinja2 for the details page.


## Running project
The current project is implemented with Python version 3.8


### Configuring Flask with environment variables

To run this application using Flask set the following environmental variables:
Linux
```
export FLASK_APP=app.py
export FLASK_ENV=development
```

Windows
```
set FLASK_APP=app.py
set FLASK_ENV=development
```

### Setting Client Id and Client Secret
The app needs Client Id and Client Secret. You can find these values in the [Customer Dashboard](https://customer-dashboard.app.authenteq.com/customer/api-keys). Pass them to the app with the environment variables:
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


### Adding redirect URL
The redirect from Web IDV can happen only to predefined addresses. Add below redirect URL in the [Customer Dashboard](https://customer-dashboard.app.authenteq.com/customer/api-keys).
```
https://localhost:5000/results
```
### Starting application
Run:
```
flask run
```


The frontend starts on port 5000 on the localhost.

Open [https://localhost:5000](https://localhost:5000).

The application contains:
* index  (/) - home page with Button which will initiate the verification process
* results (/results) displays the results of the verification
