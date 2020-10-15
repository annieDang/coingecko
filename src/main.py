import wx
import wx.grid as gridlib
from pycoingecko import CoinGeckoAPI
import pandas as pd
from win10toast import ToastNotifier

notifier = ToastNotifier()
def sendNotifications(msg):
    notifier.show_toast("Coingecko", msg, icon_path=None,duration=1000,threaded=True)
    
class Application(wx.Frame):
    def __init__(self, parent, title, pos, size):
        super(Application, self).__init__(parent, title=title, pos=pos, size=size)

        self.InitUI()
        self.Centre()
        # load data
        self.cg = CoinGeckoAPI()
        self.Layout()
        self.Update()


    def InitUI(self):
        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(15)

        self.grid_count_row = 1
        self.grid_count_col = 1

        sizer = wx.GridBagSizer(7, 5)

        text1 = wx.StaticText(panel, label="Scrape data from coingecko api")
        sizer.Add(text1, pos=(0, 0), span=(1, 3), flag=wx.LEFT|wx.CENTER, border=15)
        
        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 6), flag=wx.EXPAND|wx.CENTER, border=10)

        # input time
        st1 = wx.StaticText(panel, label='Time (in days)', size=(150, 30))
        st1.SetFont(font)
        sizer.Add(st1, pos=(2, 0), flag=wx.LEFT|wx.EXPAND|wx.CENTER,border=15)

        time_input_options = ["1h", "24h", "7d", "14d", "30d", "200d", "1y"]
        self.price_change_percentage = wx.ComboBox(panel, value=time_input_options[0], choices = time_input_options, size=(200, 30)) 
        sizer.Add(self.price_change_percentage, pos=(2, 1), span=(1, 3), flag=wx.CENTER|wx.EXPAND, border=5)

        btn1 = wx.Button(panel, label='Check', size=(70, 30))
        sizer.Add(btn1, pos=(2, 5),flag=wx.RIGHT|wx.CENTER, border=5)
        btn1.Bind(wx.EVT_BUTTON, self.check) 
        btn2 = wx.Button(panel, label='Update', size=(70, 30))
        sizer.Add(btn2, pos=(3, 5),flag=wx.RIGHT|wx.CENTER, border=5)
        btn2.Bind(wx.EVT_BUTTON, self.update) 
        
        cal_options = [ "Decreased more than", "Increased more than"]
        self.cal_combo = wx.ComboBox(panel ,value=cal_options[1] ,choices = cal_options, size=(150, 30)) 
        sizer.Add(self.cal_combo, pos=(3, 0),flag=wx.LEFT|wx.EXPAND|wx.CENTER, border=15)
        
        self.change_percentage = wx.TextCtrl(panel, value="0.5", size=(150, 30))
        sizer.Add(self.change_percentage, pos=(3, 1), flag=wx.CENTER|wx.EXPAND, border=5)
        st2 = wx.StaticText(panel, label='%', size=(30, 30))
        st2.SetFont(font)
        sizer.Add(st2, pos=(3, 2), flag=wx.LEFT|wx.CENTER,border=5)

        line2 = wx.StaticLine(panel)
        sizer.Add(line2, pos=(4, 0), span=(0, 6), flag=wx.EXPAND|wx.CENTER, border=10)

        st3 = wx.StaticText(panel, label='Result:', size=(150, 30))
        st3.SetFont(font)
        sizer.Add(st3, pos=(5, 0), flag=wx.LEFT|wx.EXPAND|wx.CENTER,border=15)
        
        self.grid = wx.grid.Grid(panel, size=(1000, 300))
        self.grid.AutoSizeColumns(setAsMin=True)
        self.grid.CreateGrid(100,12)
        sizer.Add(self.grid, pos=(6, 0), span=(0, 6), flag=wx.EXPAND|wx.CENTER, border=10)

        panel.SetSizer(sizer)
        sizer.Fit(self)


    def check(self, event):
        df_coins = pd.DataFrame(self.cg.get_coins())

        coin_list = df_coins["id"].tolist() 

        req1_field = self.price_change_percentage.GetValue()
        print(req1_field)
        req2_field = "price_change_percentage_%s_in_currency" % (req1_field)
        percent = float(self.change_percentage.GetValue())

        data = self.cg.get_coins_markets(ids=coin_list,
             vs_currency="usd", 
             price_change_percentage=req1_field)

        df_requested_data =  pd.DataFrame(data)
        if(self.cal_combo.GetValue() == "Increased more than"):
            df_requested_data = df_requested_data.loc[(df_requested_data[req2_field] > percent)]
        else:
            df_requested_data = df_requested_data.loc[(df_requested_data[req2_field] < percent)]
        # print(df_requested_data[['id', req2_field]])
        self.df_to_list(df_requested_data[['id', req2_field]])

    def df_to_list(self,df):
        print(df)
        self.clear_grid()
        self.grid_count_row, self.grid_count_col = df.shape
        print(self.grid_count_row)
        if (self.grid_count_row <= 1 or self.grid_count_col <= 1):
            return

        for x in range(len(df.columns.values)):
            self.grid.SetCellValue(0,x, str(df.columns.values[x]))
            self.grid.SetCellFont(0,x, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)) 
            self.grid.SetCellBackgroundColour(0,x, "light blue")
            self.grid.SetColSize(x, 300)
        
        row_indx = 1
        for index, row in df.iterrows():
            for col in range(0, self.grid_count_col):
                self.grid.SetCellValue(row_indx, col, str(row[col]))
            row_indx +=1
        
        self.grid.ForceRefresh()

    def clear_grid(self):
        """
        remove all data
        """
        for row in range(0,self.grid_count_row):
            for col in range(0,self.grid_count_col):
                self.grid.SetCellValue(row, col, "")
        self.grid.ForceRefresh()

    def update(self, event):
        self.clear_grid()
        self.grid.ForceRefresh()

def main():
    app = wx.App()
    ex = Application(None, title='Coingecko', pos=(50, 60), size=(1000, 500))
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()