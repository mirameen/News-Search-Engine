from tkinter import *
from tkinter import ttk
from query import *

results = []
labels = []
messages = []
srt_label = ""
fl = 0
srt = 0


def frame_con(canvas):              # configuring canvas
    canvas.configure(scrollregion=canvas.bbox("all"))


def retrieve_input():               # get input query from textbox
    query_gui = search_text.get("1.0",'end-1c')
    return query_gui


def update_gui():                   # update search results
    global fl, labels, results, messages, srt
    #print(fl)
    if fl > 0:
        srt_label['text'] = ("Search Results:-                                                                                                                            Search time:- {}".format(srt))
        for i in range(10):
            labels[i]['text'] = results[i][0]
            messages[i]['text'] = results[i][1]
    root.after(1000, update_gui)


def get_results():                  # generate search results
    global fl, srt_label, srt
    global results, labels, messages
    gui_query = retrieve_input()
    print(gui_query)
    (results, srt) = get_cos_similarity(gui_query)
    if fl == 0:
        srt_label = Label(root,text="Search Results:-                                                                                                                            Search time:- {}".format(srt))
        srt_label.pack(padx=10, pady=10)
        for i in range(10):
            ttk.Separator(root, orient='horizontal').pack(side='top', fill='x', padx=10, pady=10)
            labels.append(Label(root, bg="light yellow", text=results[i][0]))
            labels[i].pack(padx=10, pady=5)
            messages.append(Message(root, bg="light yellow", justify="left", anchor="w", width=700, text=results[i][1]))
            messages[i].pack(padx=10, pady=10)
    fl += 1


frame = Tk()
frame.geometry("800x500")
canvas = Canvas(frame, borderwidth=0, background="#d4c6c5")
root = Frame(canvas, background="#d4c6c5")
vsb = Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side=RIGHT, fill='y')
canvas.pack(side=LEFT, fill="both", expand=True)
canvas.create_window((4, 4), window=root, anchor='nw')

frame.bind("<Configure>", lambda event, canvas=canvas: frame_con(canvas))

search_text = Text(root, height=1.5)
search_text.pack(padx=10, pady=10)


search_button = Button(root, bg="light cyan", text="Search", width=15, height=2, command=get_results)
search_button.pack(padx=10, pady=20)
root.after(1000, update_gui)


frame.mainloop()
