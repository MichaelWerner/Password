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

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Password Generator", size=(700, 400))

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
        self.load_button = wx.Button(panel, label="Load File",style=wx.BORDER_NONE)
        self.load_button.SetBackgroundColour("#007BFF")  # Blue
        self.load_button.SetForegroundColour("white")
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_file)
        hbox1.Add(self.load_button, flag=wx.LEFT | wx.ALIGN_CENTER, border=5)

        # "Generate Passwords" Button
        self.ok_button = wx.Button(panel, label="Generate Passwords",style=wx.BORDER_NONE)
        self.ok_button.SetBackgroundColour("#28A745")  # Green
        self.ok_button.SetForegroundColour("white")
        self.ok_button.Bind(wx.EVT_BUTTON, self.run_script)
        hbox1.Add(self.ok_button, flag=wx.LEFT | wx.ALIGN_CENTER, border=5)

        # "Exit" Button
        self.cancel_button = wx.Button(panel, label="Exit",style=wx.BORDER_NONE)
        self.cancel_button.SetBackgroundColour("#DC3545")  # Red
        self.cancel_button.SetForegroundColour("white")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.close_app)
        hbox1.Add(self.cancel_button, flag=wx.LEFT | wx.ALIGN_CENTER, border=5)

        # Add row to the main layout
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)

        # Output box
        self.output_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 200))
        vbox.Add(self.output_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Set panel layout
        panel.SetSizer(vbox)

        # Center the window
        self.Centre()

    def on_load_file(self, event):
        """Open file dialog and load file path into text box"""
        with wx.FileDialog(self, "Select a word list file", wildcard="Word list files (wordlist*.txt)|wordlist*.txt|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User canceled
            
            # Get the selected file path and update text control
            self.file_text.SetValue(file_dialog.GetPath())

    def run_script(self, event):
        """Run the Python script with the selected file as a parameter"""
        filepath = self.file_text.GetValue()
        if filepath:
            try:
                # Set the script name
                script_name = script_path + "\password_generator_list.py"
                result = subprocess.run(["python", script_name, filepath], capture_output=True, text=True)
                self.output_text.SetValue(result.stdout)
                if result.stderr:
                    self.output_text.AppendText("\nERROR:\n" + result.stderr)
            except Exception as e:
                self.output_text.SetValue(f"ERROR: {str(e)}")

    def close_app(self, event):
        """Close the application"""
        self.Close()

# Run the application
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
