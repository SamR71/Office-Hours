# Uh-OH!
A Repository For Professor + TA Office Hours At Rensselaer Polytechnic Institute (RPI).

# Installation Procedure For Uh-OH!
Currently, Uh-OH! supports all Mac, Linux, and Unix Based Operating Systems.
Note: For Unix Based Systems, replace `pip` with `pip3`, and `python` with `python3`.
1. Clone the GitHub Repository, or simply, copy all files in this GitHub Repository to a folder on your computer.
2. Install the Latest Version of Python3. To do this, download the Latest Version from https://www.python.org/downloads/ and follow the instructions in the installer. As of right now, the Latest Version is Python 3.8.2.
3. Install Virtual Environment, pipenv, by running `pip install pipenv`. 
4. Install NodeJS (i.e., npm) by following the instructions from here: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm. 
5. Install the Django Framework by following the instructions from here: https://docs.djangoproject.com/en/3.0/intro/install/.
6. Now, navigate to the Uh-OH/frontend Directory. 
6. Install ReactJS by running the following command: `npm install react --save` in your Terminal. 
6. Run `npm install react-scripts --save` in your Terminal.
7. Run `npm install react-week-calendar --save` in your Terminal.
8. Run `npm install moment --save` in your Terminal.
9. Run `npm install bootstrap --save` in your Terminal.

# Running The Uh-OH! Website
1. To launch the Virtual Environment for the Backend, navigate to the Main Uh-OH Directory. Now, simply run `pipenv shell`. 
2. To launch the Backend Server, first navigate to Uh-OH/backend Directory. Once there, subsequently run `pip install django-cors-headers` as well as `pip install djangorestframework`. Finally, run `python manage.py runserver`.
3. To launch the Frontend Client, navigate to the Uh-OH/frontend Directory. At last, run `npm start`.
4. You should now be able to view and interact with the Main Uh-OH! Website. Welcome To Uh-OH! 


