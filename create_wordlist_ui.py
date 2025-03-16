import wx
import subprocess
import configparser
import os

# Function to read config file
def read_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

# Load configuration
config = read_config()
script_path = config.get("Settings", "script_path")
wlfolder = config.get("Settings", "wordlist_folder")

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Create Wordlist", size=(600, 150))

        # Set background color
        self.SetBackgroundColour("#d0d0d0")

        # Create a panel
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # File selection UI (TextBox + "Load File" Button)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # Text control for file path (instead of FilePickerCtrl)
        self.file_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        hbox1.Add(self.file_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # "Load File" button
        self.load_button = wx.Button(panel, label="Load Text File",style=wx.BORDER_NONE)
        self.load_button.SetBackgroundColour("#007BFF")  # Blue
        self.load_button.SetForegroundColour("white")
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_file)
        hbox1.Add(self.load_button, flag=wx.LEFT | wx.ALIGN_CENTER, border=5)

        # "Create Wordlist" Button
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(panel, label="Create Wordlist",style=wx.BORDER_NONE)
        self.ok_button.SetBackgroundColour("#28A745")  # Green
        self.ok_button.SetForegroundColour("white")
        self.ok_button.Bind(wx.EVT_BUTTON, self.run_script)


        # "Exit" Button
        self.cancel_button = wx.Button(panel, label="Exit",style=wx.BORDER_NONE)
        self.cancel_button.SetBackgroundColour("#DC3545")  # Red
        self.cancel_button.SetForegroundColour("white")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.close_app)

        hbox2.AddStretchSpacer()
        hbox2.Add(self.ok_button, flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        hbox2.Add(self.cancel_button, flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        hbox2.AddStretchSpacer()

        # Add row to the main layout
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.ALL, border=10)

        # Set panel layout
        panel.SetSizer(vbox)

        # Center the window
        self.Centre()

    def on_load_file(self, event):
        """Open file dialog and load file path into text box"""
        with wx.FileDialog(self, "Select a word list file", defaultDir=wlfolder,wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User canceled
            
            # Get the selected file path and update text control
            self.file_text.SetValue(file_dialog.GetPath())

    def run_script(self, event):
        input_filepath = self.file_text.GetValue()
        if input_filepath:
  
            try:
                input_filename = os.path.basename(input_filepath)
                input_directory = os.path.dirname(input_filepath)
                result = subprocess.run(["python", script_path, input_filepath], capture_output=True, text=True)
                if result.stderr:
                    wx.MessageBox("Error: " + result.stderr, "Create Word List", wx.ICON_ERROR)
                else:
                    wx.MessageBox(input_directory + "\wordlist_" + input_filename + " created successfully!", "Create Word List", wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"ERROR: {str(e)}", "Error", wx.ICON_ERROR)

    def close_app(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
