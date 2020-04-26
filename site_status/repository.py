from typing import List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from config import database_config

from .model import CheckEntity, SiteCheckRecord

INSERT_SITE_QUERY = "insert into site(name, url, created_date) values (%s, %s, current_date)"
INSERT_SITE_CHECK_QUERY = """insert into site_status(site_id, time, http_status_code, http_reason, response_time, created_date)
  values (%(site_id)s, %(time)s, %(http_status)s, %(http_reason)s, %(response_time)s, current_date)"""
FIND_SITE_ID_QUERY = "select id from site where name=%s"
FIND_LATEST_SITE_CHECK_QUERY = """
  select ss.id as id, ss.site_id as site_id, ss.time as time,
    ss.http_status_code as status_code, ss.http_reason as http_reason,
    ss.response_time as response_time
  from site_status ss
    inner join site s on s.id = ss.site_id
  where ss.site_id=%s
  order by ss.time desc
  fetch first row only
"""
FIND_SITE_CHECK_RECORDS_QUERY = """
  select ss.id as id, ss.site_id as site_id, ss.time as time,
    ss.http_status_code as status_code, ss.http_reason as http_reason,
    ss.response_time as response_time, s.name as name, s.url as url
  from site_status ss
    inner join site s on s.id = ss.site_id
  where s.name = %(name)s
  order by ss.time desc
"""


class StatusRepository:
    @staticmethod
    def open_connection():
        return psycopg2.connect(host=database_config["host"],
                                port=database_config["port"],
                                sslmode="require",
                                database=database_config["database"],
                                user=database_config["user"],
                                password=database_config["password"])

    @staticmethod
    def find_site_id(connection, name: str) -> Optional[int]:
        with connection.cursor() as cursor:
            cursor.execute(FIND_SITE_ID_QUERY, (name, ))
            row = cursor.fetchone()
            return None if row is None else row[0]

    @staticmethod
    def create_site_record(connection, name: str, url: str) -> Optional[int]:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_SITE_QUERY, (name, url))

        return StatusRepository.find_site_id(connection, name)

    @staticmethod
    def create_site_check_record(connection,
                                 entity: CheckEntity) -> Optional[CheckEntity]:
        with connection.cursor() as cursor:
            cursor.execute(
                INSERT_SITE_CHECK_QUERY, {
                    "site_id": entity.site_id,
                    "time": entity.check_time,
                    "http_status": entity.http_status_code,
                    "http_reason": entity.http_status_reason,
                    "response_time": entity.response_time,
                })

        return StatusRepository.find_latest_site_check(connection,
                                                       entity.site_id)

    @staticmethod
    def find_latest_site_check(connection,
                               site_id: int) -> Optional[CheckEntity]:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(FIND_LATEST_SITE_CHECK_QUERY, (site_id, ))
            row = cursor.fetchone()

            return None if row is None else CheckEntity(
                id=row["id"],
                site_id=row["site_id"],
                check_time=row["time"],
                http_status_code=row["status_code"],
                http_status_reason=row["http_reason"],
                response_time=row["response_time"])

    @staticmethod
    def find_site_check_records(connection,
                                name: str) -> List[SiteCheckRecord]:
        def to_check_record(row) -> SiteCheckRecord:
            return SiteCheckRecord(id=row["id"],
                                   site_id=row["site_id"],
                                   check_time=row["time"],
                                   http_status_code=row["status_code"],
                                   http_status_reason=row["http_reason"],
                                   response_time=row["response_time"],
                                   name=row["name"],
                                   url=row["url"])

        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(FIND_SITE_CHECK_RECORDS_QUERY, {"name": name})
            return [to_check_record(row) for row in cursor.fetchall()]
