from tkinter import *
from tkinter import ttk
import time
from datetime import timedelta

root = Tk()
root.title("Day Counter")

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, stick=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

names = ["Dias", "Horas", "Minutos", "Segundos"]
time_label = []
for i in range(4):
	time_label.append(ttk.Label(mainframe, text = names[i]))
	time_label[i].grid(column=i, row=0, padx=2, pady=2)
time_delta = []
for i in range(4):
	time_delta.append(ttk.Label(mainframe, text = "", relief='raised', font = "Helvetica 44 bold", anchor='center', padding='7 7 7 0'))
	time_delta[i].grid(column=i, row=1, padx=2, pady=2, stick=(N, W, E, S))

def handle_bad_date(wd):
	dismiss(wd)
	actioB("Data invalida")

def dismiss(wd):
    wd.grab_release()
    wd.destroy()
 
def new_target(wd, selectors):
	global target_date
	new_date = selectors[0].get() + "-" + format(selectors[1].current()+1, '02d') + "-" + selectors[2].get() + "-00-00"
	try:
		target_date = time.mktime(time.strptime(new_date, "%Y-%m-%d-%H-%M"))
		open("saved_date.txt", "w").write(new_date)
		printable = new_date.split('-')
		ate.configure(text = "até " + printable[2] + "/" + printable[1] + "/" + printable[0] + " às " + printable[3] + ":" + printable[4])
		dismiss(wd)
	except ValueError:
		handle_bad_date(wd)

def actioB(error=""):
	dlg = Toplevel(root)
	day_var = StringVar()
	day_sel = ttk.Combobox(dlg, textvariable=day_var, width = 8)
	month_var = StringVar()
	month_sel = ttk.Combobox(dlg, textvariable=month_var, width = 8)
	year_var = StringVar()
	year_sel = ttk.Combobox(dlg, textvariable=year_var, width = 8)
	day_sel.grid(column=0, row=1, padx=2, pady=5)
	month_sel.grid(column=1, row=1, padx=2, pady=5)
	year_sel.grid(column=2, row=1, padx=2, pady=5)
	day_sel.state(["readonly"])
	month_sel.state(["readonly"])
	year_sel.state(["readonly"])
	day_sel['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
	month_sel['values'] = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
	anno_domini = time.localtime()[0]
	year_sel['values'] = (anno_domini,anno_domini+1,anno_domini+2,anno_domini+3,anno_domini+4)
	selectors = [year_sel, month_sel, day_sel]
	ttk.Label(dlg, text = "Dia").grid(column=0, row=0)
	ttk.Label(dlg, text="Mês").grid(column=1, row=0)
	ttk.Label(dlg, text="Ano").grid(column=2, row=0)
	ttk.Button(dlg, text="Cancelar", command=lambda: dismiss(dlg)).grid(column = 1, row=2, padx=5, pady=5)
	ttk.Button(dlg, text="Atualizar", command=lambda: new_target(dlg, selectors)).grid(column=2, row=2, padx=5, pady=5)
	ttk.Label(dlg, text=error, foreground='red').grid(column=0, row=2, pady=5)
	dlg.protocol("WM_DELETE_WINDOW", lambda: dismiss(dlg)) # intercept close button
	dlg.transient(root)   # dialog window is related to main
	dlg.wait_visibility() # can't grab until window appears, so we wait
	dlg.grab_set()        # ensure all input goes to our window
	dlg.wait_window()     # block until window is destroyed

	
def print_hierarchy(w, depth=0):
    print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth+1)


leButon = ttk.Button(mainframe, text="Mudar", command=actioB)
leButon.grid(column=3, row=2)
ate = ttk.Label(mainframe, text = "", anchor='center')
ate.grid(column=0, row=2, columnspan=3)
#target_date = 0 #time.mktime(time.strptime("2021-06-06-12-12", "%Y-%m-%d-%H-%M"))


def clockcount():
	current_date = time.time()
	delta = timedelta(seconds=target_date-current_date)
	delta_value = []
	delta_value.append(delta.days)
	delta_value.append(int(delta.seconds / 3600))
	delta_value.append(int((delta.seconds % 3600)/60))
	delta_value.append(delta.seconds % 60)
	for i in range(4):
		time_delta[i].configure(text = format(delta_value[i], '02d'))
	mainframe.after(500, clockcount)
	
try:
	old_date = open("saved_date.txt").read()
	target_date = time.mktime(time.strptime(old_date[:-1], "%Y-%m-%d-%H-%M"))
	printable = old_date.split('-')
	ate.configure(text = "até " + printable[2] + "/" + printable[1] + "/" + printable[0] + " às " + printable[3] + ":" + printable[4])
	clockcount()
	root.mainloop()
except:
	print("Algo deu errado")



