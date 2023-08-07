# Asset Tracker
This project has been developed to automate asset management/tracking system for system admins.

# Prerequisites & Installation
1. First Clone the repository(HTTPS URL: https://github.com/Mihir1720/assignment.git).
2. Open the cloned project folder in any of the code editor.
3. Install Python3+. (Download link: https://www.python.org/downloads/)
4. Install pip(pip is a python package installer). (Download link: https://pip.pypa.io/en/stable/installation/)
5. Once python and pip are installed, open a terminal from the same location and create virtual environment by executing 'python -m venv atenv' - we can give any name to virtual environment. If we are using Linux system then we need to install virtualenv package then we can execute the given command.
6. Once virtual environment is created, in the same terminal, we have to activate created virtual environment, for that execute for Linux/MacOS: 'source atenv/bin/activate' & for Windows: 'source atenv/Scripts/activate'
7. Once virtual environment is activated, execute 'pip install -r requirements.txt' - This is to install all required packages for the project.
8. At last, open a new terminal from same location and execute python manage.py runserver
9. If the project is not deployed then we need to setup local database as well, for that
    1. Install MySQL Server
        for Linux: https://www.devart.com/dbforge/mysql/how-to-install-mysql-on-ubuntu/
    2. Once all the steps mentioned in the doc are completed, install Table+ to view databases. (Download link: https://tableplus.com/blog/2019/10/tableplus-linux-installation.html)
    3. Create database named 'asset_tracker'.
    4. Once database is created, in new terminal, execute 'python manage.py migrate'.
10. To generate seeder data do the following:
    1. Open a new terminal.
    2. Execute 'python manage.py shell'
    3. Execute 'from authentication.seed_data import seed_data
    4. Execute 'seed_data()' - It will generate 10 users by default with some random data for authentication.

