#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 09:44:42

import dbm

dbpth = './db/keysdb'

def inset(key,value):
    db = dbm.open(dbpth, 'c')
    db[key] = value
    db.close()

def delet(key):
    db = dbm.open(dbpth, 'c')
    if db.has_key(key):
        del db[key]
    db.close()

def update(key,value):
    db = dbm.open(dbpth, 'c')
    db[key] = value
    db.close()

def select(key):
    db = dbm.open(dbpth, 'c')
    if db.has_key(key):
        return db[key]
    else:
        return None
    db.close()

def allKeys():
    db = dbm.open(dbpth, 'c')
    return db.keys() 
    db.close()

def main():
    print allKeys()
    inset('mykey2', '111')
    print select('mykey')
    delet('mykey')
    print select('mykey')
    print select('mykey2')
    update('mykey2', 'dddx')
    print select('mykey2')
    # delet('mykey2')
    print allKeys()

if __name__=="__main__":  
    main()

