-- Creating cyclones table
CREATE TABLE IF NOT EXISTS cyclones (
    id varchar(255) primary key,
    created_at timestamp,
    external_id varchar(255),
    name text,
    region varchar(50),
    external_link text
);


-- Creating forecast_track table
CREATE TABLE IF NOT EXISTS forecast_tracks (
    id BIGSERIAL primary key,
    cyclone_id varchar(255) references public.cyclones(id) on delete cascade,
    created_at timestamp,
    forecast_at timestamp,
    forecast_hour numeric,
    latitude numeric,
    longitude numeric,
    intensity numeric,
    unique(cyclone_id, forecast_at, forecast_hour)
);


-- Creating track_history table
CREATE TABLE IF NOT EXISTS track_historys (
    id BIGSERIAL primary key,
    cyclone_id varchar(255) references public.cyclones(id) on delete cascade,
    created_at timestamp,
    synoptic_time timestamp,
    latitude numeric,
    longitude numeric,
    intensity numeric,
    unique(cyclone_id, synoptic_time)
);