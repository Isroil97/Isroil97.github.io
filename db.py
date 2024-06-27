import sqlite3

# User bot


def create_user_bot_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_bot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            name TEXT,
            type INTEGER NULL,
            admin INTEGER NULL,
            ban INTEGER NULL
        )
    """
    )
    conn.commit()
    conn.close()


# Create the user_bot table
create_user_bot_table()


# User qoshish
def insert_user_bot_row(id_user, name):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_bot (user_id, name)
        VALUES (?, ?)
    """,
        (id_user, name),
    )
    conn.commit()
    conn.close()


# Userdi chaqirish
def view_user_bot_table_id(id):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM user_bot WHERE user_id = ?
    """,
        (id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# foydalanuvchilar soni
def view_auser_all_bot_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM user_bot
    """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# Kanallar
def create_chanel_bot_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chanel_bot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chanel_id TEXT,
            name TEXT,
            url TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Jadvalni yaratish
create_chanel_bot_table()


# Funksiya asosida ma'lumot qo'shish
def insert_chanel_bot_row(id_chanel, name, url):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO chanel_bot (chanel_id, name, url)
        VALUES (?, ?, ?)
    """,
        (id_chanel, name, url),
    )
    conn.commit()
    conn.close()


def update_channel_bot_url(bot_id, new_url):
    try:
        with sqlite3.connect("admin_bot.db") as conn:
            cursor = conn.cursor()
            # Validate if bot_id exists in the table
            cursor.execute("SELECT COUNT(*) FROM chanel_bot WHERE id = ?", (bot_id,))
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                print(f"Bot ID {bot_id} does not exist in the database.")
                return False
            # Execute the update statement
            cursor.execute(
                """
                UPDATE chanel_bot
                SET url = ?
                WHERE id = ?
                """,
                (new_url, bot_id)
            )
            conn.commit()
        print(f"URL updated successfully for Bot ID {bot_id}.")
        return True
    except sqlite3.Error as e:
        # Log the error for debugging
        print("An error occurred:", e)
        return False



# Funksiya asosida ma'lumot o'chirish
def delete_chanel_bot_row(id):
    try:
        conn = sqlite3.connect("admin_bot.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM chanel_bot
            WHERE id = ?
        """,
            (id,),
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Xatolik yuz berdi:", e)
        return False
    finally:
        conn.close()


# Funksiya asosida ma'lumot ko'rish
def view_chanel_bot_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM chanel_bot
    """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# Admin table
def view_chanel_bot_table_id(id):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM chanel_bot WHERE id = ?
    """,
        (id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def increment_all_chanel_bot_counts():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, count FROM chanel_bot")
    rows = cursor.fetchall()
    
    for row in rows:
        if row[1] is None:
            new_count = 1
        else:
            try:
                new_count = int(row[1]) + 1
            except ValueError:
                new_count = 1

        
        cursor.execute("UPDATE chanel_bot SET count = ? WHERE id = ?", (new_count, row[0]))

    conn.commit()
    conn.close()

# Kinolar uchun
def create_movies_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_message INTEGER,
            name TEXT CHECK(length(name) <= 1000) NULL
        )
    """
    )
    conn.commit()
    conn.close()


def update_movie_table_id(id_message, new_name):
    # Veritabanı bağlantısını oluştur
    try:
        conn = sqlite3.connect("admin_bot.db")
        cursor = conn.cursor()

        # Belirli bir film kaydının adını güncelle
        cursor.execute(
            """
            UPDATE movies
            SET name = ?
            WHERE id_message = ?
        """,
            (new_name, id_message),
        )

        # Değişiklikleri kaydet ve bağlantıyı kapat
        conn.commit()
        conn.close()
    except Exception as e:
        # Hata durumunda hatayı yakalayarak yazdır
        print("Hata oluştu:", e)


def delete_movie_row(id):
    try:
        conn = sqlite3.connect("admin_bot.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM movies
            WHERE id_message = ?
        """,
            (id,),
        )
        conn.commit()
        if cursor.rowcount > 0:  # Agar o'chirish amalga oshirilgan bo'lsa
            print("Qator muvaffaqiyatli o'chirildi")
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Xatolik yuz berdi:", e)
        return False
    finally:
        conn.close()


def view_movie_all_bot_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM movies
    """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# Jadvalni yaratish
create_movies_table()


# Funksiya asosida ma'lumot qo'shish
def create_movie(id_message, caption):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO movies (id_message, name)
        VALUES (?, ?)
    """,
        (id_message, caption),
    )
    conn.commit()
    inserted_row_id = cursor.lastrowid
    conn.close()
    return inserted_row_id


def view_movie_id(id):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM movies WHERE id = ?
    """,
        (id,),
    )
    rows = cursor.fetchall()
    conn.close()  # Bağlantıyı kapatmadan önce işlem yapmak istiyorsanız burada yapabilirsiniz.
    return rows


def view_movie_message_id(id):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM movies WHERE id_message = ?
    """,
        (id,),
    )
    rows = cursor.fetchall()
    conn.close()  # Bağlantıyı kapatmadan önce işlem yapmak istiyorsanız burada yapabilirsiniz.
    return rows


# Funksiya asosida admin_bot jadvalini yaratish
def create_admin_bot_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS admin_bot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_admin INTEGER,
            name TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Jadvalni yaratish
create_admin_bot_table()


# Funksiya asosida ma'lumot qo'shish
def insert_admin_bot_row(id_admin, name):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO admin_bot (id_admin, name)
        VALUES (?, ?)
    """,
        (id_admin, name),
    )
    conn.commit()
    conn.close()


# Funksiya asosida ma'lumot o'chirish
def delete_admin_bot_row(id):
    try:
        conn = sqlite3.connect("admin_bot.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM admin_bot
            WHERE id = ?
        """,
            (id,),
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Xatolik yuz berdi:", e)
        return False
    finally:
        conn.close()


# Funksiya asosida ma'lumot ko'rish
def view_admin_bot_table():
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM admin_bot
    """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def view_admin_bot_table_id(id):
    conn = sqlite3.connect("admin_bot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM admin_bot WHERE id = ?
    """,
        (id,),
    )
    rows = cursor.fetchall()
    conn.close()  # Bağlantıyı kapatmadan önce işlem yapmak istiyorsanız burada yapabilirsiniz.
    return rows
