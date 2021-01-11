import pymysql


class DAO:
    def __init__(self, host, database, user, password):
        self._host = host
        self._database = database
        self.user = user
        self.password = password
        self._conn = self.create_connection()

    def create_connection(self):
        return pymysql.connect(host=self._host,
                       database=self._database,
                       user=self.user,
                       password=self.password,
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor
                )

    def get_connection(self):
        if self._conn is None:
            self._conn = self.create_connection()
        return self._conn

    def write(self, sql, *param):
        with self as conn:
            curs = conn.cursor()
            ok = curs.execute(sql, *param)

        return {'rows': ok}

    def write_with_conn(self, conn, sql, *param):
        curs = conn.cursor()
        return curs.execute(sql, *param)

    def read(self, sql, *param):
        conn = self.get_connection()

        curs = conn.cursor()
        curs.execute(sql, *param)

        rows = curs.fetchall()
        conn.close()
        self._conn = None

        return rows

    def read_with_conn(self, conn, sql, *param):
        curs = conn.cursor()
        curs.execute(sql, *param)

        return curs.fetchall()

    def __enter__(self):
        return self.get_connection()

    def __exit__(self, type, value, traceback):

        if type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
            print('failure to save', value)

        self._conn.close()
        self._conn = None
