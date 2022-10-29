import sqlite3
from pathlib import Path

# Initial local file config
dbname = "LOTR_DB.db"
dbfolder = "db/"

# Create the local database folder if it doesn't exist
Path(dbfolder).mkdir(parents=True, exist_ok=True)


def sqlite_connect():
    """
    Create a local connection to the local database
    """

    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)
    conn.row_factory = lambda cursor, row: row[0]


def init_sqlite():
    """
    Connect to the local database and initialize the VizzyTDB and all tables.
        """

    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE vizzy_comments (id text)''')
    c.execute('''CREATE TABLE bobby_comments (id text)''')
    c.execute('''CREATE TABLE stanny_comments (id text)''')
    c.execute('''CREATE TABLE jonny_comments (id text)''')
    c.execute('''CREATE TABLE hound_comments (id text)''')
    c.execute('''CREATE TABLE cersi_comments (id text)''')
    c.execute('''CREATE TABLE tormund_comments (id text)''')
    c.execute('''CREATE TABLE tyrion_comments (id text)''')
    c.execute('''CREATE TABLE tywin_comments (id text)''')
    c.execute('''CREATE TABLE nightking_comments (id text)''')
    c.execute('''CREATE TABLE caraxes_comments (id text)''')
    c.execute('''CREATE TABLE aeggy_comments (id text)''')
    c.execute('''CREATE TABLE sara_comments (id text)''')
    c.execute('''CREATE TABLE olenna_comments (id text)''')

def makeNewTable(name='karl'):
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE {}_comments (id text)'''.format(name))


def getComments(table):
    """Get all comment IDs from the comments table

    :return list: All comment IDs.
    """
    sqlite_connect()
    c = conn.cursor()
    c.execute("""SELECT id FROM {}""".format(table))
    result = c.fetchall()
    return result


def writeComment(id, table):
    """Write a comment ID to the comments table
    :param str id:  The comment ID to record
    """
    sqlite_connect()
    c = conn.cursor()
    q = [(id)]
    c.execute('''INSERT INTO {}('id') VALUES(?)'''.format(table), q)
    conn.commit()
    conn.close()


# Initialize the database if it's not already done
try:
    makeNewTable('merry')
except:
    pass
