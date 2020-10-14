import wx

class coingecko(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "Coingecko", size = (300, 200))
        panel=wx.Panel(self)

        status = self.CreateStatusBar()
        menuBar=wx.MenuBar()
        first=wx.Menu()
        second=wx.Menu()
        first.Append(wx.NewId(), "New Window", "This is a new windnewow")
        first.Append(wx.NewId(), "Open..", "This is a  window")
        menuBar.Append(first, "File")
        menuBar.Append(second, "Second")
        self.SetMenuBar(menuBar)
        languages = ['C', 'C++', 'Python', 'Java', 'Perl'] 
        self.combo = wx.ComboBox(panel,choices = languages) 
        self.choice = wx.Choice(panel,choices = languages)
        # self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo) 
        # self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)


        button=wx.Button(panel, label="exit", pos=(10, 10), size=(60,60))
        self.Bind(wx.EVT_BUTTON, self.closeButton, button)
        self.Bind(wx.EVT_CLOSE, self.closeWindow)

    def closeButton(self, event):
        self.Close(True)

    def closeWindow(self, event):
        self.Destroy()
    
if __name__== '__main__':
    app = wx.PySimpleApp()
    frame=coingecko(parent=None, id =-1)
    frame.Show()
    app.MainLoop()