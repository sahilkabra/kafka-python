import psycopg2
from typing import Optional

from config import database_config

from .model import CheckEntity

INSERT_SITE_QUERY = "insert into site(name, url, created_date) values (%s, %s, current_date)"
INSERT_SITE_CHECK_QUERY = """insert into site_status(site_id, time, http_status_code, http_reason, response_time, created_date)
                                values (%(site_id)s, %(time)s, %(http_status)s, %(http_reason)s, %(response_time)s, current_date)"""
FIND_SITE_ID_QUERY = "select id from site where name=%s"
FIND_SITE_CHECK_QUERY = """select id, site_id, time, http_status_code, http_reason, response_time
                            from site_status
                            where
                            site_id=%s
                            order by time desc
                            fetch first row only
                            """


class StatusRepository:
    def open_connection(self):
        self.connection = psycopg2.connect(
            host=database_config["host"],
            port=database_config["port"],
            sslmode="require",
            database=database_config["database"],
            user=database_config["user"],
            password=database_config["password"])

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def find_site_id(self, name: str) -> Optional[int]:
        with self.connection.cursor() as cursor:
            cursor.execute(FIND_SITE_ID_QUERY, (name, ))
            row = cursor.fetchone()
            return None if row is None else row[0]

    def create_site_record(self, name: str, url: str) -> Optional[int]:
        with self.connection.cursor() as cursor:
            cursor.execute(INSERT_SITE_QUERY, (name, url))

        return self.find_site_id(name)

    def create_site_check_record(self,
                                 entity: CheckEntity) -> Optional[CheckEntity]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                INSERT_SITE_CHECK_QUERY, {
                    "site_id": entity.site_id,
                    "time": entity.check_time,
                    "http_status": entity.http_status_code,
                    "http_reason": entity.http_status_reason,
                    "response_time": entity.response_time,
                })

        return self.find_latest_site_check(entity.site_id)

    def find_latest_site_check(self, site_id: int) -> Optional[CheckEntity]:
        with self.connection.cursor() as cursor:
            cursor.execute(FIND_SITE_CHECK_QUERY, (site_id, ))
            row = cursor.fetchone()

            return None if row is None else CheckEntity(
                id=row[0],
                site_id=row[1],
                check_time=row[2],
                http_status_code=row[3],
                http_status_reason=row[4],
                response_time=row[5])
