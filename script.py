#!/usr/bin/env python
# -*- coding: latin-1 -*-

import os
import sqlite3


def parse(guid):
    return guid.split(";")[2]


def getContacts():
    messages_db = os.path.expanduser('~') + "/Library/Messages/chat.db"
    conn = sqlite3.connect(messages_db)
    cursor = conn.cursor()
    select_statement = ("SELECT chat.guid FROM chat;")
    cursor.execute(select_statement)
    results = cursor.fetchall()
    conn.close()
    guids = set()
    for result in results:
        guids.add(parse(result[0]))
    return guids


def main():
    contactArray = getContacts()
    print(contactArray)


main()
