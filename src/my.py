import wx
import wx.grid as gridlib
from pycoingecko import CoinGeckoAPI
import pandas as pd

class Application(wx.Frame):
    def __init__(self, parent, title, pos, size):
        super(Application, self).__init__(parent, title=title, pos=pos, size=size)

        self.InitUI()
        self.Centre()
        # load data
        self.cg = CoinGeckoAPI()


    def InitUI(self):
        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(15)

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
        time_combo = wx.ComboBox(panel,choices = time_input_options, size=(200, 30)) 
        time_combo.Bind(wx.EVT_COMBOBOX, self.onTimeCombo) 
        sizer.Add(time_combo, pos=(2, 1), span=(1, 3), flag=wx.CENTER|wx.EXPAND, border=5)

        btn1 = wx.Button(panel, label='Check', size=(70, 30))
        sizer.Add(btn1, pos=(2, 5),flag=wx.RIGHT|wx.CENTER, border=5)
        btn2 = wx.Button(panel, label='Update', size=(70, 30))
        sizer.Add(btn2, pos=(3, 5),flag=wx.RIGHT|wx.CENTER, border=5)
        
        cal_options = [ "Decreased more than", "Increased more than"]
        cal_combo = wx.ComboBox(panel,choices = cal_options, size=(150, 30)) 
        cal_combo.Bind(wx.EVT_COMBOBOX, self.onTimeCombo) 
        sizer.Add(cal_combo, pos=(3, 0),flag=wx.LEFT|wx.EXPAND|wx.CENTER, border=15)
        
        tc2 = wx.TextCtrl(panel, size=(150, 30))
        sizer.Add(tc2, pos=(3, 1), flag=wx.CENTER|wx.EXPAND, border=5)
        st2 = wx.StaticText(panel, label='%', size=(30, 30))
        st2.SetFont(font)
        sizer.Add(st2, pos=(3, 2), flag=wx.LEFT|wx.CENTER,border=5)

        line2 = wx.StaticLine(panel)
        sizer.Add(line2, pos=(4, 0), span=(0, 6), flag=wx.EXPAND|wx.CENTER, border=10)

        st3 = wx.StaticText(panel, label='Result:', size=(150, 30))
        st3.SetFont(font)
        sizer.Add(st3, pos=(5, 0), flag=wx.LEFT|wx.EXPAND|wx.CENTER,border=15)

        grid = wx.grid.Grid(panel, size=(1000, 300))
        grid.CreateGrid(15,12)
        sizer.Add(grid, pos=(6, 0), span=(0, 6), flag=wx.EXPAND|wx.CENTER, border=10)

        panel.SetSizer(sizer)
        sizer.Fit(self)

    def onTimeCombo(self, event):
        df_coins = pd.DataFrame(self.cg.get_coins())

        coin_list = df_coins["id"].tolist()
        print(coin_list)
        print("combo")


def main():
    app = wx.App()
    ex = Application(None, title='Coingecko', pos=(50, 60), size=(1000, 500))
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()