from copy import deepcopy
import operator
import pymysql


class Connections:
    """
    Record different configs of connection to DB
    """
    # connection config of Huang Hongzhao
    Newaser = {
        'host': 'localhost',
        'user': 'root',
        'password': '147258',
        'database': 'core_ooc_db',
        'charset': 'utf8',
    }

    # connection config of Feng Hongding
    Feng = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123456',
        'database': 'core_ooc_db',
        'charset': 'utf8',
    }

    @classmethod
    def have(cls, connection):
        """If ':param:`connection`' is one of the connections
        """
        for internal_connection in cls.__dict__.values():
            if operator.eq(connection, internal_connection):
                return True
        return False

    @classmethod
    def modified(cls, connect, **kwargs):
        """Return a modified edition of a connection
        """
        if not cls.have(connect):
            raise ValueError('''
            Invalid connection name is given. The name must be one of the defined one.
            ''')

        new_connect = deepcopy(connect)
        for key, value in kwargs.items():
            if key not in connect.keys():
                raise ValueError(f'''
                No configuration called {key} in current connection
                ''')
            new_connect[key] = value

        return new_connect


# Set default Connection
DEFAULT_CONNECT = Connections.Newaser


def fetch(connection, sql):
    """Fetch query results of 'sql' from DB with 'connection'
    """
    conn = pymysql.connect(**connection)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()

    return data


def get_field_list(connection, table_name):
    """Get all fields(columns) of a certain table
    """
    info_connect = Connections.modified(connection, database='information_schema')

    sql = "SELECT COLUMN_NAME " \
          "FROM COLUMNS " \
          f"WHERE table_name = '{table_name}'"
    data = fetch(info_connect, sql)

    return [ele[0] for ele in data]
