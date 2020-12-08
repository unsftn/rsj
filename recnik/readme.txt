How to set up:
    - Be sure you have the latest docker & docker-compose version

    1. For initial test purposes change the following settings:
        - In Dockerfile change django_settings value from 'prod' to 'test' (later on you should change this to 'dev' value while developing)
        - In run_prod.sh file change DJANGO_SETTINGS from 'prod' to 'test' (later on you should change this to 'dev' value while developing)
        - In uwsgi-prod.ini file change DJANGO_SETTINGS from 'prod' to 'test' (later on you should change this to 'dev' value while developing)
    
    2. in project root folder (recnik) run following commands:
        - sudo docker build --tag recnik:1.0 .
        - sudo docker run --publish 8000:8000 recnik:1.0
    After this your test app should be running on localhost:8000, and admin panel is available at localhost:8000/admin

    3. Now that we tested our config, let's create dev environment.
        - In project root folder check file called docker-compose.yml
        - Check env variables for mySQL connection. My SQL server is docker image so we don't need it locally running.
        - There's two services in this file. One is to setup database and the other one to start the application.
    If everything is okay, run following command:
        - sudo docker-compose up
        This command will fire up all services needed (db & web)
        If everything is okay, you should have running app on localhost:8000