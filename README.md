## Cyclone Crawling service 

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

####  Database Schema 
There are three tables that store the information related to current cyclones - 

Cyclones - stores information about the cyclones that are live

```
Table "public.cyclones"
    Column     |            Type            
---------------+----------------------------
 id                  | character varying(255)  
 created_at    | timestamp without time zone 
 external_id   | character varying(255)   
 name          | text                        
 region        | character varying(50)    
 external_link | text
 
 ```
---

forecast_tracks - stores the forecasted track of the cyclone 

```
Table "public.forecast_tracks"
    Column     |            Type            
---------------+---------------------------
 id                  | bigint                     
 cyclone_id    | character varying(255)     
 created_at    | timestamp without time zone
 forecast_at   | timestamp without time zone 
 forecast_hour | numeric                    
 latitude      | numeric                    
 longitude     | numeric                    
 intensity     | numeric                   
track_historys | stores the history of how the cyclone is moving
```
---

```
Table "public.track_historys"
    Column     |            Type            
---------------+----------------------------
 id            | bigint                      
 cyclone_id    | character varying(255)   
 created_at    | timestamp without time zone 
 synoptic_time | timestamp without time zone
 latitude      | numeric                   
 longitude     | numeric                 
 intensity     | numeric 
 ```
---

#### Engineering design 

There are five containers running - 
- Main server (serves rest api to query about cyclone data) - Flask
- Worker (responsible for scraping data) - Flask, Celery
- Scheduler (that triggers the task to scrape data every hour) - Celery beat
- Redis (that serves as the broker for celery)
- Postgresql Db (the database that stores information about the cyclones)

Every hour the scheduler sends a task to the worker using the queue. The worker picks the task from the queue and executes it. 
The worker is responsible for getting the data by crawling over the link and saving in the database.
The server serves endpoints to query about the cyclone information.


##### APIs

/cyclones: Method - GET

Response - List of cyclones saved in the db. 

```
{
  count: n,
  data: [{cyclone_object}]
}
```

/cyclones/<cyclone_id/forecast_tracks: Method - GET

Response - List of forecast_tracks for a particular cyclone saved in the db. 

```
{
  count: n, 
  data: [{forecast_track_object}]
}
```

/cyclones/<cyclone_id/track_historys: Method - GET
	
Response - List of track_historys for a particular cyclone saved in the db. 
```
{
  count: n, 
  data: [{track_history_object}]
}
```

ASSUMPTIONS:
- Only scraping data for the live cyclones and not the old ones. 
- Not saving any other information that is available in the form of images. 

---
