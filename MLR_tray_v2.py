import wx.adv
import sys
import wx
MLR_TOOLTIP = 'MLR Defense' 
MLR_ICON = 'icon.png' 

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        #def status bar
        self.CreateStatusBar()
        
        #def menu bar
        appMenu = wx.Menu()
        
        #def menu items
        menuAbout = appMenu.Append(wx.ID_ABOUT, "&About","This application has been developed to practically apply machine learning to prevent ransomware.")
        menuExit = appMenu.Append(wx.ID_EXIT,"&Exit","Close MLR Defense")

        #creating menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(appMenu,"&File")
        self.SetMenuBar(menuBar)

        #def menu binds
        self.Bind(wx.EVT_MENU, self.OnAbout,menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        #spawning window
        self.SetIcon(wx.Icon(MLR_ICON))
        self.Show(True)

    def OnAbout(self, event):
        #opens a dialog box with information about the application
        aboutdlg = wx.MessageDialog(self, "This application has been developed to apply machine learning to ransomware prevention. Developed by Bradley Silva and Justin Crozier.", caption="About")
        aboutdlg.ShowModal()
        aboutdlg.Destroy()

    def OnExit(self, event):
        #closes the application

        sys.exit()

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        #def tray frame
        self.frame = frame
        super(TaskBarIcon, self).__init__()

        #setting tray icon
        self.set_icon(MLR_ICON)

        #setting left click bind
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        #def tray menu
        menu = wx.Menu()
        menu.AppendSeparator()
        
        #def tray menu items
        create_menu_item(menu, 'Open', self.on_open)
        create_menu_item(menu, 'Exit', self.on_exit)
        
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, MLR_TOOLTIP)
    
    def on_left_down(self, event):
        app = wx.App(False)
        frame = MainWindow(None, "MLR Defense")
        app.MainLoop()

    def on_open(self, event):      
        app = wx.App(False)
        frame = MainWindow(None, "MLR Defense")
        app.MainLoop()

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()