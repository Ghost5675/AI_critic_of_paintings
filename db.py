import sqlite3


# Класс для управления базой данных картин
class ArtDatabase:
    def __init__(self, db_name="art_gallery.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицу для авторов картин
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS creators (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE)''')

        # Создаем таблицу для картин с уникальным ID и ссылкой на автора
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS paintings (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                creator_id INTEGER,
                                FOREIGN KEY (creator_id) REFERENCES creators(id))''')

        # Создаем таблицу для критериев оценивания
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS criteria (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE)''')

        # Создаем таблицу для хранения оценок по критериям
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (
                                painting_id INTEGER,
                                criterion_id INTEGER,
                                rating INTEGER,
                                FOREIGN KEY (painting_id) REFERENCES paintings(id),
                                FOREIGN KEY (criterion_id) REFERENCES criteria(id))''')
        self.connection.commit()

    def add_creator(self, creator_name):
        # Добавляем нового создателя картины, если его нет в базе
        self.cursor.execute('''INSERT OR IGNORE INTO creators (name)
                               VALUES (?)''', (creator_name,))
        self.connection.commit()

        # Получаем ID создателя после добавления
        self.cursor.execute('''SELECT id FROM creators WHERE name = ?''', (creator_name,))
        return self.cursor.fetchone()[0]

    def add_painting(self, name, creator_name):
        # Получаем ID создателя или добавляем нового
        creator_id = self.add_creator(creator_name)

        # Добавляем новую картину с указанием ID создателя
        self.cursor.execute('''INSERT INTO paintings (name, creator_id)
                               VALUES (?, ?)''', (name, creator_id))
        self.connection.commit()

    def add_criterion(self, criterion_name):
        self.cursor.execute('''INSERT INTO criteria (name)
                               VALUES (?)''', (criterion_name,))
        self.connection.commit()

    def rate_painting(self, painting_id, criterion_id, rating):
        self.cursor.execute('''INSERT INTO ratings (painting_id, criterion_id, rating)
                               VALUES (?, ?, ?)''', (painting_id, criterion_id, rating))
        self.connection.commit()

    def get_paintings(self):
        # Получаем список всех картин с их ID, названиями и авторами
        self.cursor.execute('''SELECT paintings.id, paintings.name, creators.name 
                               FROM paintings
                               JOIN creators ON paintings.creator_id = creators.id''')
        return self.cursor.fetchall()

    def get_criteria(self):
        self.cursor.execute('''SELECT id, name FROM criteria''')
        return self.cursor.fetchall()

    def get_all_ratings(self):
        # Получаем всю информацию о картинах, критериях и оценках
        self.cursor.execute('''
            SELECT paintings.id, paintings.name, creators.name, criteria.name, ratings.rating
            FROM ratings
            JOIN paintings ON ratings.painting_id = paintings.id
            JOIN criteria ON ratings.criterion_id = criteria.id
            JOIN creators ON paintings.creator_id = creators.id
        ''')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


# Пример использования:
if __name__ == "__main__":
    db = ArtDatabase()

    # Добавляем картину с именем создателя
    db.add_painting("Звездная ночь", "Алишер")

    # Оценки картины по критериям
    paintings = db.get_paintings()
    criteria = db.get_criteria()

    # db.rate_painting(paintings[0][0], criteria[0][0], 1)
    # db.rate_painting(paintings[0][0], criteria[1][0], 2)

    # Вывод всей таблицы с оценками
    all_ratings = db.get_all_ratings()
    print("\nПолная таблица оценок:")
    for rating in all_ratings:
        print(
            f"ID картины: {rating[0]}, Картина: {rating[1]}, Создатель: {rating[2]}, Критерий: {rating[3]}, Оценка: {rating[4]}")

    db.close()