import myUI as UI
import tkinter as tk

root = tk.Tk()
root.title("test")
root.minsize(796,816)
root.geometry("1920x1080")
root.state('zoomed')
app = UI.MyApp(master=root)
app.mainloop()