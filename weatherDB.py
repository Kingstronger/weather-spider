import sqlite3
import  datetime
import time

#id int primary key autoincrement,
def createWeatherDB(c):
    c.execute('''create table weather
            (positionId int not null,
            name text not null,
            date_time date not null,
            temperature int,
            rain int,
            humidity int,
            windDirection int,
            windPower int,            
            fullName text not null,
            createTime text not null DEFAULT (datetime('now','localtime')));''')

def createPositionDB(c):
    c.execute('''create table position
            (positionId int not null,
            name text not null,
            fullName text not null);''')

conn = sqlite3.connect("demo.db")
c = conn.cursor()
createWeatherDB(c)
# createPositionDB(c)


