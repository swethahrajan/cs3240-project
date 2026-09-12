[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/F1hjDb63)


Heroku CLI commands:

push to heroku:
git push heroku main

run migrations on heroku postgres:
heroku run python manage.py migrate

stop server:
heroku ps:scale web=0

start server:
heroku ps:scale web=1