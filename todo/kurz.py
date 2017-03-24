from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

import sqlite3



# notes = {
#     0: 'do the shopping',
#     1: 'build the codez',
#     2: 'paint the door',
# }


def note_repr(key):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos WHERE Id = " + str(key))
    row = cur.fetchone()
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'text': row[1]
    }


@app.route("/", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    if request.method == 'POST':
        note = str(request.data.get('text', ''))
        # idx = max(notes.keys()) + 1

        cur.execute("INSERT INTO todos VALUES (?, ?)", (None, note,))
        cur.execute("SELECT * FROM todos ORDER BY Id DESC LIMIT 1")
        idx = cur.fetchone()[0]
        conn.commit()

        # notes[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    cur.execute("SELECT * FROM todos")
    rows = cur.fetchall()
    keys = [i[0] for i in rows]
    cur.close()
    conn.close()
    return [note_repr(idx) for idx in sorted(keys)]


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        notes[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS todos (Id INTEGER PRIMARY KEY AUTOINCREMENT, todo_text TEXT)")
    app.run(debug=True)
    cur.close()
    conn.close()
