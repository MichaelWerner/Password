import wx
import subprocess

class ShadowButton(wx.Panel):
    def __init__(self, parent, label="Click Me", pos=(50, 50), size=(150, 40), shadow_offset=(3, 3), on_click=None):
        super().__init__(parent, pos=pos, size=size, style=wx.BORDER_NONE)
        self.label = label
        self.shadow_offset = shadow_offset
        self.on_click = on_click
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click_event)

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        width, height = self.GetSize()

        # Improved shadow effect
        shadow_color = wx.Colour(50, 50, 50, 80)
        gc.SetBrush(wx.Brush(shadow_color))
        gc.SetPen(wx.Pen(shadow_color, 0))
        gc.DrawRoundedRectangle(self.shadow_offset[0], self.shadow_offset[1], width - 4, height - 4, 12)

        # Button background
        button_color = wx.Colour(40, 120, 220)
        gc.SetBrush(wx.Brush(button_color))
        gc.SetPen(wx.Pen(button_color, 0))
        gc.DrawRoundedRectangle(0, 0, width - 4, height - 4, 12)

        # Draw text
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        gc.SetFont(font, wx.WHITE)
        tw, th = gc.GetTextExtent(self.label)
        gc.DrawText(self.label, (width - tw) / 2, (height - th) / 2)

    def on_click_event(self, event):
        if self.on_click:
            self.on_click(event)

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Python Script UI", size=(600, 400))
        self.SetBackgroundColour("#d0d0d0")
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # File selection UI
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_picker = wx.FilePickerCtrl(panel, message="Select a word list file", wildcard="Word list files (wordlist*.txt)|wordlist*.txt|All files (*.*)|*.*")
        hbox1.Add(self.file_picker, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)

        # Buttons
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = ShadowButton(panel, label="Generate Passwords", on_click=self.run_script, pos=(20, 80))
        self.cancel_button = ShadowButton(panel, label="Exit", on_click=self.close_app, pos=(200, 80))

        hbox2.Add(self.ok_button, flag=wx.RIGHT, border=10)
        hbox2.Add(self.cancel_button)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Output box
        self.output_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 200))
        vbox.Add(self.output_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Centre()

    def run_script(self, event):
        filepath = self.file_picker.GetPath()
        if filepath:
            try:
                result = subprocess.run(["python", "C:\\Users\\micha\\OneDrive\\Documents\\Repositories\\Python\\password\\password_generator_list.py", filepath], capture_output=True, text=True)
                self.output_text.SetValue(result.stdout)
                if result.stderr:
                    self.output_text.AppendText("\nERROR:\n" + result.stderr)
            except Exception as e:
                self.output_text.SetValue(f"ERROR: {str(e)}")

    def close_app(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
