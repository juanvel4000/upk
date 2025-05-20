import sqlite3
from . import variables
import sqlite3
from . import variables

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(variables.database)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                version TEXT NOT NULL,
                manifest TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def isPackageInstalled(self, package):
        self.cur.execute("SELECT 1 FROM packages WHERE name = ?", (package,))
        return self.cur.fetchone() is not None

    def checkPackageVersion(self, package):
        self.cur.execute("SELECT version FROM packages WHERE name = ?", (package,))
        row = self.cur.fetchone()
        return row[0] if row else None
    def insertPackage(self, name, version, manifest, pkgstr=None):
        if pkgstr == None:
            pkgstr = f"local/{name}:{version}"
        self.cur.execute("INSERT INTO packages (name, version, manifest) VALUES (?, ?, ?)", (name, version, manifest))
        self.conn.commit()
    def deletePackage(self, name):
        self.cur.execute("DELETE FROM packages WHERE name = ?", (name,))
        self.conn.commit()
    def getPackageManifest(self, package):
        self.cur.execute("SELECT manifest FROM packages WHERE name = ?", (package,))
        row = self.cur.fetchone()
        return row[0] if row else None