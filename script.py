#!/usr/bin/env python
# -*- coding: latin-1 -*-

import os
from pathlib import Path
import sqlite3


def main():
    # Connect to db
    messages_db = os.path.expanduser('~') + "/Library/Messages/chat.db"
    conn = sqlite3.connect(messages_db)
    cursor = conn.cursor()

    # Get contacts
    select_statement = ("SELECT chat_identifier FROM chat;")
    cursor.execute(select_statement)
    results = cursor.fetchall()
    contacts = set()
    for result in results:
        contacts.add(result[0])

    # Create messages folder
    path = Path('./Messages')
    os.makedirs(path, exist_ok=True)

    # Get messages for each contact
    for contact in contacts:
        print("Getting messages for " + contact + "...")

        # SQL query get messages
        select_statement = ("SELECT is_from_me, text, datetime(date + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date FROM message WHERE NOT is_delivered = 0 AND handle_id IN (SELECT ROWID FROM handle WHERE id = '" + contact + "') ORDER BY date;")
        cursor.execute(select_statement)
        results = cursor.fetchall()

        if len(results) == 0:
            continue

        # Create contact file
        file_path = './Messages/' + contact + '.txt'
        with open(file_path, 'w+') as f:
            for result in results:
                f.write(result[2] + " ")
                if result[0]:
                    f.write("Me: ")
                else:
                    f.write(contact + ": ")
                if result[1] is not None:
                    f.write(result[1])
                f.write("\n")

    conn.close()

    print("iMessage parsing complete")


main()
