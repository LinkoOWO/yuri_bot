import sqlite3, random

conn = sqlite3.connect("vocabulary.db")
cursor = conn.cursor()

def sqlrecreate():
    cursor.execute("""
    DROP TABLE IF EXISTS words
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voc TEXT NOT NULL CHECK(LENGTH(voc) <= 100),
        pos TEXT NOT NULL CHECK(LENGTH(pos) <= 4),
        mean TEXT CHECK(LENGTH(mean) <= 100)
    )
    """)
    conn.commit()
    print("RECREATE SUCCESSFUL")
    
def sqlinsert(voc, pos, mean):
    if len(voc)>100 or len(pos)>4 or len(mean)>100:
        return 1

    cursor.execute("SELECT * FROM words WHERE voc = ? AND pos = ?", (voc, pos))
    existing_word = cursor.fetchone()

    if not existing_word:
        cursor.execute("INSERT INTO words (voc, pos, mean) VALUES (?, ?, ?)",(voc, pos, mean))
        conn.commit()
        return 0
    else:
        return 2
    
def sqlsearchE_prefix(voc):
    try:
        cursor.execute("SELECT * FROM words WHERE voc = ?", (voc,))
        results = cursor.fetchall()
        if results:
            return results
        else:
            print("NO SUCH WORD")
            return 3
    except:
        try:
            cursor.execute("SELECT * FROM words WHERE voc LIKE ?", (voc + '%',))
            results = cursor.fetchall()
            if results:
                return results
            else:
                print("NO SUCH WORD")
                return 3
        except:
            return 7

def sqlsearchC(mean):
    cursor.execute("SELECT * FROM words WHERE mean LIKE ?", ('%' + mean + '%',))
    results = cursor.fetchall()
    if results:
        return results
    else:
        print("NO SUCH WORD")
        return 3
    
def sqldelete(voc, pos, mean, double=0):
    if double == 0:
        return -1
    elif double == 1:
        cursor.execute("DELETE FROM words WHERE voc = ? AND pos = ? AND mean = ?", (voc, pos, mean))
        conn.commit()
        return 0
    else:
        return 4
    
def question(times):
 
    cursor.execute("SELECT * FROM words")
    all_words = cursor.fetchall()

    if not all_words:
        return []

    times = min(times, len(all_words))

    selected = random.sample(all_words, times)

    return selected

def sqlsearch(voc, pos):
    cursor.execute("SELECT * FROM words WHERE voc = ? AND pos = ?", (voc, pos))
    existing_word = cursor.fetchone()
    if existing_word:
        return existing_word
    else:
        print("NO SUCH WORD")
        return 3

def sqlrenew_mean(voc, pos, mean):
    cursor.execute("UPDATE words SET mean = ? WHERE voc = ? AND pos = ?", (mean, voc, pos))
    conn.commit()
    return 0

def sqlshowall():
    cursor.execute("SELECT * FROM words")
    all_words = cursor.fetchall()
    return all_words

def sqlupdate(voc, pos, mean):
    cursor.execute("UPDATE words SET mean = ? WHERE voc = ? AND pos = ?", (mean, voc, pos))
    conn.commit()
    return 0