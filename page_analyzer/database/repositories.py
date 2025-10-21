from page_analyzer.models import Url, UrlChecks


class UrlRepository:
    def __init__(self, connection):
        self.conn = connection

    def save(self, url: Url):
        with self.conn.cursor() as cur:
            if url.id is None:
                cur.execute('''
                INSERT INTO urls (name, created_at) 
                VALUES (%s, NOW()) 
                RETURNING id, created_at;
                ''', (url.name, ))

                res = cur.fetchone()
                url.id = res['id']
                url.created_at = res['created_at']
        return url

    def find(self, url_id: int = None, url_name: str = None) -> Url | None:
        with self.conn.cursor() as cur:
            if url_name:
                placeholder = url_name
                sql = "SELECT * FROM urls WHERE name = %s;"
            else:
                placeholder = url_id
                sql = "SELECT * FROM urls WHERE id = %s;"
            cur.execute(sql, (placeholder,))
            res = cur.fetchone()
            if not res:
                return None
            return Url(id=res['id'], name=res['name'], created_at=res['created_at'])

    def get_all(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, created_at FROM urls ORDER BY created_at DESC;")
            res = cur.fetchall()
            for row in res:
                yield Url(id=row['id'], name=row['name'], created_at=row['created_at'])


class UrlChecksRepository:
    def __init__(self, connection):
        self.conn = connection

    def save(self, url: Url):
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO url_checks (url_id, created_at)
                VALUES (%s, NOW())
                RETURNING id, created_at;
                ''', (url.id, ))

            res = cur.fetchone()
            return UrlChecks(
                id=res['id'],
                url_id=url.id,
                created_at=res['created_at'])

    def get_all(self, url: Url):
        with self.conn.cursor() as cur:
            cur.execute('''
            SELECT 
                * 
            FROM url_checks
            WHERE url_id = %s
            ORDER BY created_at DESC;
            ''', (url.id,))

            res = cur.fetchall()
            for row in res:
                yield UrlChecks(
                    id=row['id'],
                    url_id=url.id,
                    created_at=row['created_at'],
                    status_code=row['status_code'],
                    h1=row['h1'],
                    title=row['title'],
                    description=row['description'])
