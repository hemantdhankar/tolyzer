# tolyzer
A tool to analyze the error and attack tolerance of a Network. Users will get a detailed analysis of the uploaded network in terms of Degree Distribution, Clustering Coefficient, Characteristic Path Length, Hubs and behavior under error or attack circumstances.

## How to Setup?
1. git pull <link_to_repo>
2. Inside the repo directory. Create a Virtual Environment named "venv" using pip (COMMAND: "virtualvenv venv")
3. Enter the virtual environment. (COMMAND: "venv\Scripts\Activate")
4. Once inside the virtual environment, install all dependencies. (COMMAND: "pip install -r requirements.txt")
5. Add yourself as a superuser (COMMAND: "django-admin createsuperuser")
6. Launch the app. (COMMAND: "python manage.py runserver")
7. Open a new terminal and run django-background-task app (COMMAND: "python manage.py process_tasks")
8. Site should be live at "localhost:8000/dashboard/"