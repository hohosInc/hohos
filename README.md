<h2>hohos</h2> 

[![Join the chat at https://gitter.im/dbads/hohos](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hohosguys/Lobby)<br>

Visit hohos - [hohos.tech](http://hohos.tech)



<h3>How to run hohos locally ?</h3><hr>
      
Clone the repo and follow these steps 

       git clone https://github.com/dbads/hohos.git

1. **Install Requirements**
   
       sudo apt-get install python3
       sudo apt-get install python3-pip python3-dev libpq-dev postgresql
       sudo apt-get install python3-setuptools
       pip3 install -r requrements.txt

       if pip doesn't work, easy_install is there for you e.g.
       $ easy_install package_name

2. **Database configuration**

       If you use postgresql then
       Change name of databse, db user, db password, localhost, and you can leave port blank

       If you want to use sqlite3 then just uncomment the sqlite configuration.

3. **Configuring Settings.py file** 

       you can make DEBUG=True while you are working locally
       ALLOWED_HOSTS=['*'] in local

4. **Sensitive Information**
     
       There are some variables which are coming from either environment variables 
       or from a file sensitive.py so you just create this file and pust those variables 
       in that file or you can use environment variables too. 

       #SENSITIVE DATABASE INFORMATION
       DB_NAME='xyz'
       DB_PASS='your_DB_PASS'
       DB_PORT=5432
       DB_USER='abc'

       #SENSITIVE EMAIL DATA
       SECRET_KEY='7yl&y17r&7h*#fk&whgdhgyys#^m$0+k$)l!-idm*md%w_ldcj'
       EMAIL_HOST='smtp.gmail.com' 
       EMAIL_HOST_USER='your Email'
       EMAIL_HOST_PASSWORD='your email password'
       EMAIL_PORT='587'

5. **Now Use the following commands to build the required tables**

       python3 manage.py migrate
       python3 manage.py makemigrations
       python3 manage.py collectstatic
       python3 manage.py createsuperuser to make a super user
       visit ip:domain/admin  to see admin panel
       
6. **Commands to run server**

       python3 manage.py runserver <ip>:<port>
       default port is 8000 and default address is 127.0.0.1
       ctrl+c to stop the server

7. **I will soon update readme telling how to deploy hohos on Heroku and Digital Ocean.**

       
*Want to add some feature in hohos, fork the hohos, make changes and create a Pull Request*
*you can always email me or come on gitter in case of any query*       
[![Join the chat at https://gitter.im/dbads/hohos](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hohosguys/Lobby)<br>

