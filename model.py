import psycopg2
import time


class MuseumGalleryExhibitModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='museum-gallery-exhibit-management-system',
            user='postgres',
            password='1234',
            host='localhost',
            port=5432
        )
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS Museum (
                Museum_ID SERIAL PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Location VARCHAR(150) NOT NULL,
                Established_Year INT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS Gallery (
                Gallery_ID SERIAL PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Floor INT,
                Theme VARCHAR(100),
                Museum_ID INT NOT NULL,
                CONSTRAINT fk_museum FOREIGN KEY (Museum_ID) REFERENCES Museum(Museum_ID)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS Exhibit (
                Exhibit_ID SERIAL PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Description TEXT,
                Year_Created INT,
                Gallery_ID INT NOT NULL,
                CONSTRAINT fk_gallery FOREIGN KEY (Gallery_ID) REFERENCES Gallery(Gallery_ID)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS Exhibit_Schedule (
                Exhibit_Schedule_ID SERIAL PRIMARY KEY,
                Start_Date DATE NOT NULL,
                End_Date DATE NOT NULL,
                Exhibit_ID INT NOT NULL,
                Gallery_ID INT NOT NULL,
                CONSTRAINT fk_exhibit FOREIGN KEY (Exhibit_ID) REFERENCES Exhibit(Exhibit_ID),
                CONSTRAINT fk_gallery_schedule FOREIGN KEY (Gallery_ID) REFERENCES Gallery(Gallery_ID)
            )
        ''')

        self.conn.commit()

    def add_museum(self, name, location, established_year):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO Museum (Name, Location, Established_Year) VALUES (%s, %s, %s)',
                      (name, location, established_year))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error adding museum: {e}")
            self.conn.rollback()

    def add_gallery(self, name, floor, theme, museum_id):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO Gallery (Name, Floor, Theme, Museum_ID) VALUES (%s, %s, %s, %s)',
                      (name, floor, theme, museum_id))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error adding gallery: {e}")
            self.conn.rollback()

    def add_exhibit(self, name, description, year_created, gallery_id):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO Exhibit (Name, Description, Year_Created, Gallery_ID) VALUES (%s, %s, %s, %s)',
                      (name, description, year_created, gallery_id))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error adding exhibit: {e}")
            self.conn.rollback()

    def add_exhibit_schedule(self, start_date, end_date, exhibit_id, gallery_id):
        try:
            c = self.conn.cursor()
            c.execute('''
                INSERT INTO Exhibit_Schedule (Start_Date, End_Date, Exhibit_ID, Gallery_ID)
                VALUES (%s, %s, %s, %s)
            ''', (start_date, end_date, exhibit_id, gallery_id))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error adding exhibit schedule: {e}")
            self.conn.rollback()

    def delete_museum(self, museum_id):
        try:
            c = self.conn.cursor()
            c.execute('DELETE FROM Museum WHERE Museum_ID=%s', (museum_id,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error deleting museum: {e}")
            self.conn.rollback()

    def delete_gallery(self, gallery_id):
        try:
            c = self.conn.cursor()
            c.execute('DELETE FROM Gallery WHERE Gallery_ID=%s', (gallery_id,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error deleting gallery: {e}")
            self.conn.rollback()

    def delete_exhibit(self, exhibit_id):
        try:
            c = self.conn.cursor()
            c.execute('DELETE FROM Exhibit WHERE Exhibit_ID=%s', (exhibit_id,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error deleting exhibit: {e}")
            self.conn.rollback()

    def delete_exhibit_schedule(self, schedule_id):
        try:
            c = self.conn.cursor()
            c.execute('DELETE FROM Exhibit_Schedule WHERE Exhibit_Schedule_ID=%s', (schedule_id,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error deleting exhibit schedule: {e}")
            self.conn.rollback()

    def get_museums(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Museum')
        return c.fetchall()

    def get_galleries(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Gallery')
        return c.fetchall()

    def get_exhibits(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Exhibit')
        return c.fetchall()

    def get_exhibit_schedule(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Exhibit_Schedule')
        return c.fetchall()

    def update_museum(self, museum_id, name, location, established_year):
        c = self.conn.cursor()
        c.execute('''
            UPDATE Museum SET Name=%s, Location=%s, Established_Year=%s WHERE Museum_ID=%s
        ''', (name, location, established_year, museum_id))
        self.conn.commit()

    def update_gallery(self, gallery_id, name, floor, theme, museum_id):
        c = self.conn.cursor()
        c.execute('''
            UPDATE Gallery SET Name=%s, Floor=%s, Theme=%s, Museum_ID=%s WHERE Gallery_ID=%s
        ''', (name, floor, theme, museum_id, gallery_id))
        self.conn.commit()

    def update_exhibit(self, exhibit_id, name, description, year_created, gallery_id):
        c = self.conn.cursor()
        c.execute('''
            UPDATE Exhibit SET Name=%s, Description=%s, Year_Created=%s, Gallery_ID=%s WHERE Exhibit_ID=%s
        ''', (name, description, year_created, gallery_id, exhibit_id))
        self.conn.commit()

    def generate_random_data(self, iterations=5):
        c = self.conn.cursor()

        for _ in range(iterations):
            # Insert one random row into Museum
            c.execute('''
                INSERT INTO Museum (Name, Location, Established_Year)
                VALUES (
                    'Museum ' || trunc(random() * 1000 + 1)::int,
                    'Location ' || trunc(random() * 100 + 1)::int,
                    (1900 + trunc(random() * 123))::int
                );
            ''')

            # Insert one random row into Gallery with valid Museum_ID
            c.execute('''
                INSERT INTO Gallery (Name, Floor, Theme, Museum_ID)
                VALUES (
                    'Gallery ' || trunc(random() * 1000 + 1)::int,
                    trunc(random() * 10 + 1)::int,
                    'Theme ' || trunc(random() * 100 + 1)::int,
                    (SELECT Museum_ID FROM Museum OFFSET floor(random() * (SELECT COUNT(*) FROM Museum)) LIMIT 1)
                );
            ''')

            # Insert one random row into Exhibit with valid Gallery_ID
            c.execute('''
                INSERT INTO Exhibit (Name, Description, Year_Created, Gallery_ID)
                VALUES (
                    'Exhibit ' || trunc(random() * 1000 + 1)::int,
                    'Description ' || trunc(random() * 1000 + 1)::int,
                    (1800 + trunc(random() * 223))::int,
                    (SELECT Gallery_ID FROM Gallery OFFSET floor(random() * (SELECT COUNT(*) FROM Gallery)) LIMIT 1)
                );
            ''')

            # Insert one random row into Exhibit_Schedule with valid Exhibit_ID and Gallery_ID
            c.execute('''
                INSERT INTO Exhibit_Schedule (Start_Date, End_Date, Exhibit_ID, Gallery_ID)
                VALUES (
                    current_date + (random() * 365)::int,
                    current_date + (random() * 365 + 365)::int,
                    (SELECT Exhibit_ID FROM Exhibit OFFSET floor(random() * (SELECT COUNT(*) FROM Exhibit)) LIMIT 1),
                    (SELECT Gallery_ID FROM Gallery OFFSET floor(random() * (SELECT COUNT(*) FROM Gallery)) LIMIT 1)
                );
            ''')

        self.conn.commit()

    def query_museum_gallery(self, location, floor):
        c = self.conn.cursor()
        start_time = time.time()
        c.execute('''
            SELECT m.Name AS Museum_Name, g.Name AS Gallery_Name, g.Floor
            FROM Museum m
            INNER JOIN Gallery g ON m.Museum_ID = g.Museum_ID
            WHERE m.Location = %s AND g.Floor = %s
            GROUP BY m.Name, g.Name, g.Floor
        ''', (location, floor))
        rows = c.fetchall()
        execution_time = (time.time() - start_time) * 1000
        return rows, execution_time

    def query_exhibit_schedule(self, start_date, end_date):
        c = self.conn.cursor()
        start_time = time.time()
        c.execute('''
            SELECT e.Name AS Exhibit_Name, s.Start_Date, s.End_Date
            FROM Exhibit e
            INNER JOIN Exhibit_Schedule s ON e.Exhibit_ID = s.Exhibit_ID
            WHERE s.Start_Date >= %s AND s.End_Date <= %s
            GROUP BY e.Name, s.Start_Date, s.End_Date
        ''', (start_date, end_date))
        rows = c.fetchall()
        execution_time = (time.time() - start_time) * 1000
        return rows, execution_time

    def query_museum_exhibit_count(self, established_year):
        c = self.conn.cursor()
        start_time = time.time()
        c.execute('''
            SELECT m.Name AS Museum_Name, COUNT(e.Exhibit_ID) AS Exhibit_Count
            FROM Museum m
            INNER JOIN Gallery g ON m.Museum_ID = g.Museum_ID
            INNER JOIN Exhibit e ON g.Gallery_ID = e.Gallery_ID
            WHERE m.Established_Year >= %s
            GROUP BY m.Name
        ''', (established_year,))
        rows = c.fetchall()
        execution_time = (time.time() - start_time) * 1000
        return rows, execution_time