import sqlite3
import uuid


class DataModel:
    download_page_url = ""
    download_url = ""
    url_trace_csv = ""
    meta_csv = ""

    def __init__(self):
        self.id = uuid.uuid4().urn


class DataAccess:
    db_conn = None

    def __init__(self):
        if not DataAccess.db_conn:
            conn = DataAccess.db_conn = sqlite3.connect('fcb-crawler.db')
            conn.execute('''create table if not exists fcb
            (
                id text, 
                download_page_url text, 
                download_url text, 
                url_trace_csv text,
                meta_csv text
            )
            ''')

        self.db_conn = DataAccess.db_conn

    def store(self, data_model):
        self.db_conn.execute(
            "insert into fcb VALUES (?, ?, ?, ?, ?)",
            [
                data_model.id,
                data_model.download_page_url,
                data_model.download_url,
                data_model.trace_url_csv,
                data_model.meta_csv
            ]
         )
        self.db_conn.commit()
