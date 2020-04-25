create table site
(
    id   serial primary key,
    name varchar,
    url  varchar,
    created_date date
);

create table site_status
(
    id               serial primary key,
    site_id          integer references site (id),
    time             timestamptz,
    http_status_code integer,
    http_reason      varchar,
    response_time    integer,
    created_date     date
);
