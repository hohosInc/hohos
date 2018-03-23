<h2 align="center">hohos</h2> 
<!-- [![Dependency Status](https://david-dm.org/dbads/hohos/status.svg?style=flat)](https://david-dm.org/dbads/hohos) [![Build Status](https://travis-ci.org/dbads/hohos.svg?branch=master)](https://travis-ci.org/dbads/hohos) [![Join the chat at https://gitter.im/dbads/hohos](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hohosguys/Lobby) -->

<!--
<a href="https://github.com/dbads/hohos"><img src="https://camo.githubusercontent.com/a34cfbf37ba6848362bf2bee0f3915c2e38b1cc1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5052732d77656c636f6d652d627269676874677265656e2e7376673f7374796c653d666c61742d737175617265" alt="PRs Welcome" data-canonical-src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" style="max-width:100%;"></a>
<a href="https://github.com/dbads/hohos"><img src="https://camo.githubusercontent.com/30fd882638a1573cd130a3021502e63038ddf342/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f41626865792f566973696f6e2e737667" alt="GitHub Stars" data-canonical-src="https://img.shields.io/github/stars/dbads/hohos.svg" style="max-width:100%;"></a>
<a href="https://github.com/dbads/hohos"><img src="https://camo.githubusercontent.com/78edf0eec50e3e0167a1169cd1a262e55f849a5a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f76657273696f6e2d312e312d677265656e2e737667" alt="Current Version" data-canonical-src="https://img.shields.io/badge/version-1.0-green.svg" style="max-width:100%;">
 -->
 <!-- [![star this repo](http://githubbadges.com/star.svg?user=dbads&repo=github-badges)](http://github.com/dbads/hohos)
[![fork this repo](http://githubbadges.com/fork.svg?user=dbads&repo=github-badges)](http://github.com/dbads/hohos/fork)
[![star this repo](http://githubbadges.com/star.svg?user=dbads&repo=github-badges&style=flat&color=fff&background=007ec6)](https://github.com/dbads/hohos)
[![fork this repo](http://githubbadges.com/fork.svg?user=dbads&repo=github-badges&style=flat&color=fff&background=007ec6)](https://github.com/dbads/hohos/fork) -->


[![Join the chat at https://gitter.im/dbads/hohos](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hohosguys/Lobby) <br>

Visit hohos - [hohos.tech](http://hohos.tech)



<h3 align="center">How to run hohos locally ?</h3> <hr>
      
      sudo apt-get install python3
      sudo apt-get install python3-pip
      pip3 install -r requrements.txt

Database configuration

     If you use postgresql then
     Change name of databse, db user, db password, localhost, and you can leave port blank
     
     If you want to use sqlite3 then just uncomment the sqlite configuration.

Configuring Settings.py file 


     you can make DEBUG=True while you are working locally
     ALLOWED_HOSTS=['*'] in local
     
Sensitive Information
     
     There are some variables which are coming from either environment variables or from a file sensitive.py 
     so you just create this file and pust those variables in that file or you can use environment variables too. 
     
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
     
