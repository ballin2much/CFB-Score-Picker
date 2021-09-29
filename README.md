# CFB Score Picker

This website is based on a competition my Dad and his friends have been doing for a very long time. The premise is that you pick a college football team and then every week you and your friends pick scores for that week's game. You then get points for picking the winner, the closest scores, and the closest spreads. I originally set this site up to only work for UNC football, but am currently working on updating to be able to support all teams.

To run the project locally clone the repo, download Docker, and navigate to the root folder. Run the following to make the migrations and start the server:
```console
ballin2much@PC:~/CFB-Score-Picker$ sudo docker-compose run web python manage.py makemigrations
ballin2much@PC:~/CFB-Score-Picker$ sudo docker-compose up
```
*If you are on WSL2 make sure to clone the repo into the WSL subsystem, otherwise you will have CHOWN issues with the Postgres Docker image.*

If you need to create an admin user:
```console
ballin2much@PC:~/CFB-Score-Picker$ sudo docker-compose run web python manage.py createsuperuser
```

Now you need to run a custom admin command in order to populate the database with team and game data from ESPN. To do so run the following
```console
ballin2much@PC:~/CFB-Score-Picker$ sudo docker-compose run web python manage.py getteams
ballin2much@PC:~/CFB-Score-Picker$ sudo docker-compose run web python manage.py getschedule 2021
```
The first line populates the database with all FBS and FCS teams, while the second command pulls every game that involves an FCS team.

You will also need to create a .env file with a value for SECRET_KEY. 