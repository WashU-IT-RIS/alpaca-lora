# On The Server

## The Database

This one is short. The database is a SQLITE database that is initialized with a handful of fields to store interactions with users. This database is currently expected to exist within the `/db` mount, but you can alter it in the `chatbot/base/views.py` folder to point wherever you want. The database itself is defined by the schema `CREATE TABLE Interactions (id BIGINT PRIMARYKEY NOT NULL, rating INT, tstamp DATETIME, ip VARCHAR(50), question TEXT, answer TEXT)`. It is necessary to "seed" the table with an entry of `id` 0 and `NULL` fields elsewhere, because I haven't worked with SQL in over six months and didn't have time to figure out how to properly initialize auto-incrementing ids. Sue me.
