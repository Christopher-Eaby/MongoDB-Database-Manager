# -*- coding: utf-8 -*-
"""
       (`-()_.-=-.
       /66  ,  ,  \
     =(o_/=//_(   /======`
         ~"` ~"~~`
Created on Thu Jul 23 09:28:47 2020
@author: Chris
"""

import pymongo #mongodb module
import pandas as pd #dataframing
import json
import tkinter as tk #gui

#creates mongodatabase and the collections
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Data_Tracker"]
mycol = mydb["SPRINT_3"]
coltop3 = mydb["Top3"]

# function to add the data to the main collection
def addalldata():
    mycol.delete_many({})
    header = None
    data = pd.read_csv('stocks.csv', header = header)   # loading csv file
    data_json = json.loads(data.to_json(orient='records'))
    mycol.insert_many(data_json)
    mydoc = mycol.find({}, { "_id": 0, "1": 1}).sort("Type")
    y = ''
    for (x) in mydoc:
        y += str(x) + "\n"
    txt.delete("1.0","end")
    
    txt.insert(tk.END, y)

# function to add the data into the top 3 collection
def addtop3():
    coltop3.delete_many({})
    header = None
    data = pd.read_csv('stocks-top.csv', header = header)   # loading csv file
    data_json = json.loads(data.to_json(orient='records'))
    coltop3.insert_many(data_json)
    mydoc = coltop3.find({}, { "_id": 0, "1": 1}).sort("Type")
    y = ''
    for (x) in mydoc:
        y += str(x) + "\n" 
    txt.delete("1.0","end")
    
    txt.insert(tk.END, y)
    
# function to delete certain data in the top 3 collection
def deletedata():
    qry1 = { "1": "Lays" }
    qry2 = { "1": "Tex" }
    
    coltop3.delete_one(qry1)
    coltop3.delete_one(qry2)
    
    y = ''
    for (x) in coltop3.find({}, { "_id": 0, "1": 1}):
        y += str(x) + "\n" 
    txt.delete("1.0","end")
    
    txt.insert(tk.END, y)

# function to update specific data in the top 3 collection
def updatedata():
    qry1 = { "1": "Simba" }
    qry2 = { "$set": { "1": "Doritos" } }

    coltop3.update_one(qry1, qry2)
    
    y = ''
    for (x) in coltop3.find({}, { "_id": 0, "1": 1}):
        y += str(x) + "\n"
    txt.delete("1.0","end")
    
    txt.insert(tk.END, y)

# function to sort through the data in DB
def sortdata():
    sort = mycol.find({}, { "_id": 0, "1": 1}).sort("1", -1)
    
    y = ''
    for (x) in sort:
        y += str(x) + "\n"
    txt.delete("1.0","end")
    
    txt.insert(tk.END, y)
    
# function to sort through the data in the top 3 DB
def sorttop3data():
    qry2 = { "1": "Tex" }
    coltop3.delete_one(qry2)
    qry1 = { "1": "Fanta" }
    coltop3.delete_one(qry1)
    
    y = ''
    
    for (x) in coltop3.find({}, { "_id": 0, "1": 1}):
        y += str(x) + "\n"
    txt.delete("1.0","end")
    
    txt.insert(tk.END, y)

gui = tk.Tk()
# sets the title 
gui.title("Database manager")
# sets the size
gui.geometry("348x200")

# text field for displaying the data
txt = tk.Text(gui, fg = "white", bg = "purple", height = 7, width = 44)
# griding for the text field
txt.grid(columnspan = 4)

# creates buttons for all the functions
b1 = tk.Button(gui, text = "Add", height = 2, width = 13, command = lambda: addalldata())
b1.grid(row = 5, column = 0) 
b1 = tk.Button(gui, text = "Add Top 3", height = 2, width = 13, command = lambda: addtop3())
b1.grid(row = 5, column = 1) 
b2 = tk.Button(gui, text = "Delete", height = 2, width = 13, command = lambda: deletedata())
b2.grid(row = 5, column = 2) 
b3 = tk.Button(gui, text = "Update", height = 2, width = 13, command = lambda: updatedata())
b3.grid(row = 6, column = 0) 
b3 = tk.Button(gui, text = "Sort", height = 2, width = 13, command = lambda: sortdata())
b3.grid(row = 6, column = 1) 
b3 = tk.Button(gui, text = "Bottom 3", height = 2, width = 13, command = lambda: sorttop3data())
b3.grid(row = 6, column = 2) 

gui.mainloop()