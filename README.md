## Database Applications and Systems Final Project ##
## Readme by Shepard Gordon and Isaac Llewellyn ##

# Instructions written assmuning the user is using Windows #

1. Using the command terminal, navgiate to the "code" folder in the final project repository
2. Run the command "pip install -r requirements.txt" to have pip install all packages needed for this project to run
3. Run the command "psql -U postgres postgres < db-setup.sql" to create the final project postgres database with a user and password. Enter your postgres password when prompted.
4. Run the command "python retrieve_data.py" to get the four datasets needed from the NY government
5. Run the command "python load_data.py" to populate the postgres db and mongodb with information pulled from the csvs in step three. This will take a few minutes to complete!
6. You're now ready to explore the datasets! Run the command "python main.py" to begin.
7. Follow the alphanumerical option commands listsed to find out more about historical sites and trout 