UBUNTUnstalled ubuntu (need to skip unattended installation or terminal won't 
        installed visual machine virtualbox
        installed ubuntu (need to skip unattended installation or terminal won't launch) 
        python works from terminal
        comfort resolution: 1280x960
        sublime text won't run if saved in google drive location somehow
        installed linux addition via terminal because shared folder didnt work:
        cd /media/iso
    sudo ./VBoxLinuxAdditions.run
        sudo adduser $USER vboxsf
VENV
        installed new python 3.8 with the help of chatbotgpt
        installed venv in this new 3.8: python3.8 -m venv myenv
SUBLIME TEXT + CONDA
        installed package control in sublime text
        installed conda in Sublime
        added directory to search for venvs for conda: 
        {
        "environment_directory": "~/Documents/Projects/",        
        }
        while venv path is: ~/Documents/Projects/venv
        then do palette: conda activate


GOOGLE REMOTE DESKTOP AND FIX BLACK SCREEN:
        Disable the Gnome display manager service on your instance, because it conflicts with the Chrome Remote Desktop service.
        sudo systemctl disable gdm3.service
        sudo reboot


        BRINGS BACK GNOME FROM BLACK SCREEN:
        /opt/google/chrome-remote-desktop/chrome-remote-desktop --stop


        systemctl start gdm3
        not working: systemctl -f enable gdm.service
not work systemctl set-default graphical.target






today i learned to do fake user agent [429]
sorting dictionary
append to list




MySQL


sudo apt install mysql-server
sudo service mysql start
sudo systemctl enable mysql
sudo service mysql status


ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pass';
CREATE USER 'evgeny'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pass';


        what helped to find mysql in python:
sudo apt install libmysqlclient-dev
sudo apt install pkg-config
pip install mysqlclient
        pip install mysql-connector-python






CREATE DATABASE AVITO_DB;
use AVITO_DB;
GRANT ALL ON *.* TO 'evgeny'@'localhost';
FLUSH PRIVILEGES;


CREATE TABLE cars (
id VARCHAR(255) PRIMARY KEY,
date TEXT,
city TEXT,
make TEXT,
model TEXT,
year INTEGER,
mileage INTEGER,
power INTEGER,
price INTEGER,
link TEXT,
type TEXT,
wd TEXT,
fuel TEXT,
comment_text TEXT
);


export your database:
mysqldump -u evgeny -p AVITO_DB > opencv.sql
Using SCP, copy over SSH your file:
scp opencv.sql evgeny@25.39.6.10:opencv2.sql
And import it (you need to create dbname before):
mysql -u evgeny -p OPEN_CV < opencv2.sql


SCRAPY SPIDER
https://docs.scrapy.org/en/latest/intro/tutorial.html#creating-a-project



SSH


DJANGO
        python manage.py runserver 95.140.153.88:80


{% load staticfiles %}


To deploy static files in Django, follow these steps:


1. First, define the static files directory in your Django project settings.py file:


```
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```


2. Create a directory named "static" in your project's root directory.


3. Inside the "static" directory, create subdirectories for each app's static files. For example, if you have an app named "blog", you can create a "blog" directory inside the "static" directory.


4. In each app's static directory, create a "static" subdirectory and place your static files there. For example, if you have a CSS file named "style.css" for your "blog" app, place it in "blog/static/blog/static/style.css".


5. In your HTML templates, load the static files using the `{% static %}` template tag. For example:


```
<link rel="stylesheet" href="{% static 'blog/static/style.css' %}">
```


6. Finally, run the `collectstatic` command to collect all static files into a single directory for deployment:


```
python manage.py collectstatic




GIT
https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners
https://selectel.ru/blog/tutorials/what-is-git-push-and-how-to-use-it/



$ git config --global user.name "your_github_username"
$ git config --global user.email "your_github_email"
$ git config -l


Once GIT is configured, we can begin using it to access GitHub. Example:


$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `YOUR-REPOSITORY`...
Username: <type your username>
Password: <type your password or personal access token (GitHub)


Now cache the given record in your computer to remembers the token:


$ git config --global credential.helper cache


COPY FILES
pscp root@95.140.153.88:/root/algo/configs/95.140.153.88/wireguard/desktop.png /home/evgeny