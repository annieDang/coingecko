import tkinter as tk
from tkinter import ttk 
from win10toast import ToastNotifier
from pycoingecko import CoinGeckoAPI
import pandas as pd
import numpy as np
import time
from tooltip import CreateToolTip
from datetime import datetime, timedelta

notifier = ToastNotifier()
def sendNotifications(msg):
    notifier.show_toast("Coingecko", msg, icon_path=None,duration=1000,threaded=True)

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Coingecko scraper")
        # Width height
        master.geometry("1200x500")

        # load data
        self.cg = CoinGeckoAPI()
        
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var


    def create_widgets(self):
        # Time range
        self.price_change_percentage = tk.StringVar()
        
        time_label = tk.Label(
            self.master, text="Time (in days)", font=("bold", 14), pady=20)
        time_label.grid(row=1, column=1, sticky=tk.W, padx=30)
        
        time_input_options =  ttk.Combobox(self.master, textvariable = self.price_change_percentage, font=("bold", 12)) 
        time_input_options["values"] = ["1h", "24h", "7d", "14d", "30d", "200d", "1y"]
        time_input_options.grid(row=1, column = 2, padx=30)
        time_input_options.current(0)
        
        # operation option
        self.opt_option = tk.StringVar()
        options = ttk.Combobox(self.master, textvariable = self.opt_option, font=("bold", 14)) 
        
        # Adding combobox drop down list 
        options["values"] = [ "Decreased more than", "Increased more than"]
        options.grid(row=2, column=1, padx=30)
        options.current(1)
        CreateToolTip(options, "in %")

        self.change_percentage = tk.StringVar()

        percentage_input =  tk.Entry(self.master, textvariable=self.change_percentage, width = 27)
        percentage_input.grid(row=2, column=2, padx=30)  

        # Filtered list (listbox)
        self.tree = ttk.Treeview(self.master)
        self.tree.grid(row=3,column=0,rowspan=1,columnspan=5)

        # Bind select
        # self.parts_list.bind("<<ListboxSelect>>", self.select_item)

        # Buttons
        check_btn = tk.Button(
            self.master, text="Check", width=12, command=self.check)
        check_btn.grid(row=1, column=3, pady=20)
        CreateToolTip(check_btn, "connect and filter all coins that pit to the conditions")

        update_btn = tk.Button(
            self.master, text="Update", width=12, command=self.update)
        update_btn.grid(row=1, column=4)

    def check(self):
        df_coins = pd.DataFrame(self.cg.get_coins())

        coin_list = df_coins["id"].tolist() 

        req1_field = self.price_change_percentage.get()
        req2_field = "price_change_percentage_%s_in_currency" % (req1_field)
        percent = int(self.change_percentage.get())

        data = self.cg.get_coins_markets(ids=coin_list,
             vs_currency="usd", 
             price_change_percentage=req1_field)

        df_requested_data =  pd.DataFrame(data)
        if(self.opt_option.get() == "Increased more than"):
            df_requested_data = df_requested_data.loc[(df_requested_data[req2_field] > percent)]
        else:
            df_requested_data = df_requested_data.loc[(df_requested_data[req2_field] < percent)]
        self.df_to_list(df_requested_data[['id', req2_field]])

    def df_to_list(self,df):
        self.tree["columns"] = df.columns.values.tolist()
        for x in range(len(df.columns.values)):
            self.tree.column(df.columns.values[x], width=100)
            self.tree.heading(df.columns.values[x], text=df.columns.values[x])

        for index, row in df.iterrows():
            self.tree.insert("",0,text=index,values=list(row))

        # self.tree.bind("<<TreeviewSelect>>", self.populate_selection)
        

    def update(self):
        sendNotifications("update")

   

root = tk.Tk()
app = Application(master=root)
app.mainloop()
