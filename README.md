# Uh-OH!
A Repository for Professor and TA Office Hours at RPI.

# Running Uh-OH!
Prerequisites: Python 3, pipenv, node/npm, react, django
1. To launch the virtual environment for the backend, navigate to the Uh-OH directory and run `pipenv shell` 
2. To launch the backend, navigate to Uh-OH/backend and run `python manage.py runserver` (or `python3 manage.py runserver` on Linux). Make sure to run `pip install django-cors-headers` and `pip3 install djangorestframework`.
3. To launch the frontend, navigate to Uh-OH/frontend and run `npm start`. Make sure to run `npm install react-scripts`.

# Additional Required Software
To display Schedule Viewer:
1. run `npm install react-week-calendar --save`
2. run `npm install moment --save`
