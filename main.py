from tkinter import filedialog
from tkinter import *
import time
import os
import Escalonador
from Escalonador import *

global logado

logado = False


dirpath = os.path.dirname(__file__)
MainWin = Tk()

logdata_file = open(dirpath+"\\System16\\SystemData\\logdata.txt","r+")
logdata = (logdata_file.read()).split("\n")


remdata_file = open(dirpath+"\\System16\\SystemData\\remdata.txt","r+")
remdata = remdata_file.read()
remdata_file.close()

def log_in(logdata, remdata):
    global logado
    username = user_var.get()
    password = pass_var.get()

    for log in logdata:
        if (log.split(" "))[0] == username:
            if (log.split(" "))[1] == password:
                if rem_var.get() == 1:
                    os.remove(dirpath+"\\System16\\SystemData\\remdata.txt")
                    remdata_file = open(dirpath + "\\System16\\SystemData\\remdata.txt", "w+")
                    remdata_file.write(f'{username} {password}')
                    remdata_file.close()
                else:
                    os.remove(dirpath + "\\System16\\SystemData\\remdata.txt")
                    remdata_file = open(dirpath + "\\System16\\SystemData\\remdata.txt", "w+")
                    remdata_file.write('0')
                    remdata_file.close()
                if int((log.split(" "))[2]) == 0:
                    logado = True
                    return MainWin.destroy()
                else:
                    logado = True
                    return MainWin.destroy()



    return incorrect.place(x=625, y=410)



# Interface Inicial
user_var = StringVar()
pass_var = StringVar()
rem_var = IntVar()
MainWin.title("Janelas Alpha 1.0")
MainWin.geometry("1280x720")
ImLog = PhotoImage(file=dirpath+"\\System16\\SystemImages\\UserLogIn.png")
MainWin.configure(background='#3B6EA5')

l_login = Label(MainWin,
                image=ImLog,
                compound='bottom'
                ).place(y=188, x=387, width=507, heigh=311)

user_entry = Entry(MainWin,
                   textvariable=user_var,
                   font=('Microsoft Sans Serif',10,'normal')
                   )

pass_entry = Entry(MainWin,
                   show="*",
                   textvariable=pass_var,
                   font=('Microsoft Sans Serif',10,'normal')
                   )

if (remdata.split(" "))[0] == "0":
    user_entry.insert(1,"username")
else:
    user_entry.insert(1, (remdata.split(" "))[0])
    pass_entry.insert(1, (remdata.split(" "))[1])

user_entry.place(x=495, y=350, width=300)
pass_entry.place(x=495, y=383, width=300)

ok_but = Button(MainWin,
                text="OK",
                command=lambda: log_in(logdata, remdata),
                background='#D4D0C8'
                )
ok_but.place(x=495, y=455, width=85)

cancel_but = Button(MainWin,
                    text="Cancel",
                    background='#D4D0C8',
                    state='disabled'
                    )
cancel_but.place(x=585, y=455, width=85)

shut_but = Button(MainWin,
                  text="Shutdown",
                  background='#D4D0C8',
                  command=lambda: MainWin.destroy(),
                  cursor='pirate'
                  )
shut_but.place(x=675, y=455, width=85)

check_box = Checkbutton(MainWin,
                        text="Lembrar Usuário",
                        background='#D4D0C8',
                        variable=rem_var
                        )
check_box.place(x=495, y=410)
check_box.select()

incorrect = Label(MainWin,
                  text="Usuário e/ou senha incorreta!",
                  font=('Microsoft Sans Serif', 10, 'normal'),
                  fg='red',
                  compound='top',
                  background='#D4D0C8'
                  )





MainWin.mainloop()

if logado == True:
    MainWinDesk = Tk()
    time_aux = time.time()
    time_var = StringVar()
    time_var.set(time.time())

    ImTB = PhotoImage(file=dirpath + "\\System16\\SystemImages\\TaskBar.png")
    l_taskbar = Label(MainWinDesk,
                      image=ImTB,
                      compound='bottom'
                      ).place(x=0, y=680, width=1280, heigh=40)

    MainWinDesk.title("Janelas Alpha 1.0")
    MainWinDesk.geometry("1280x720")
    MainWinDesk.configure(background='#3B6EA5')

    escIcon = PhotoImage(file=dirpath + "\\System16\\SystemImages\\exeIcon.png")
    l_esc = Button(MainWinDesk,
                   text="Escalonador.exe",
                   image=escIcon,
                   compound='bottom',
                   bd=0,
                   cursor='hand2',
                   relief='solid',  bg='#3B6EA5',
                   activebackground='#5980a9',
                   command=EscalonarWin
                   ).grid(column=0, row=0, padx=5, pady=5)

    escIluIcon = PhotoImage(file=dirpath + "\\System16\\SystemImages\\exe2Icon.png")
    l_escIlu = Button(MainWinDesk,
                   text="Escalonador\nIlustrativo.exe",
                   image=escIluIcon,
                   compound='bottom',
                   bd=0,
                   cursor='hand2',
                   relief='solid', bg='#3B6EA5',
                   activebackground='#5980a9',
                   state='disabled'
                   ).grid(column=0, row=1, padx=5, pady=5)

    while logado:

        l_time = Label(MainWinDesk,
                       text=str(f"{time.ctime(time_aux).split(' ')[3]}\n{time.ctime(time_aux).split(' ')[0]+' '+time.ctime(time_aux).split(' ')[2]+' '+time.ctime(time_aux).split(' ')[1]+' '+time.ctime(time_aux).split(' ')[4]}"),
                       background='#d4d0c7',
                       font=('Microsoft Sans Serif', 7, 'normal'),
                       relief='sunken'
                       )
        l_time.place(x=1149, y=685, width=127)

        ImMix = PhotoImage(file=dirpath + "\\System16\\SystemImages\\Audio.png")
        l_mixer = Label(MainWinDesk,
                          image=ImMix,
                          compound='bottom',
                          background='#d4d0c7',
                          ).place(x=1152, y=688, width=24, heigh=24)

        time_aux = time.time()
        MainWinDesk.update_idletasks()
        MainWinDesk.update()
        time.sleep(0.01)
        l_time.destroy()