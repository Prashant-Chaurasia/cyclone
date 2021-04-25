Service that crawls and stores the live cyclone information in the database.
  
#### How to run

Make sure you have docker installed in your system. 

- Open a terminal, go to the project directory and run -  
```
docker-compose up -d
```
- To verify if the services are running or not, run `docker-compose ps` and you should see all the containers with state as Up. 
```
(master) $ docker-compose ps
       Name                      Command               State           Ports
-------------------------------------------------------------------------------------
cyclone_db_1          docker-entrypoint.sh postgres    Up      5432/tcp
cyclone_redis_1       docker-entrypoint.sh redis ...   Up      6379/tcp
cyclone_scheduler_1   celery -A service.server.c ...   Up      7007/tcp
cyclone_server_1      /bin/ash run_server.sh           Up      0.0.0.0:7007->7007/tcp
cyclone_worker_1      celery -A service.server.c ...   Up      7007/tcp
```
