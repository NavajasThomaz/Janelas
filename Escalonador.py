import random
import time
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from geradorEntrada import GenerateProcess
import os

global type_var, clock_var, ent_var, pri_var, alt_var, lot_var, cfs_var
dirpath = os.path.dirname(__file__)


def PriorizarOld(processos):
    org = []
    for processo in processos:
        if org == []:
            org.append(processo)
        else:
            for i in range(len(org) + 1):
                if int(processo[3]) > int((org[i])[3]):
                    org.insert(i, processo)
                    break
                elif int(processo[3]) == int((org[i])[3]):
                    if int(processo[2]) < int((org[i])[2]):
                        org.insert(i, processo)
                        break
                    else:
                        org.insert(i + 1, processo)
                        break
                org.append(processo)
                break

    return org


def Priorizar(processos):
    org = []
    for j in range(1, 100, 1):
        org += [[j, ], ]
    for processo in processos:
        for num in org:
            if num[0] == int(processo[3]):
                num.append(processo)
    return org


def Escalonar(tipo, pos_esc, prop_label):

    # interface
    prop_label.delete('1.0', END)

    # Receber os processos
    dirpath = os.path.dirname(__file__)
    entrada = open(dirpath + '\\System16\\SystemData\\temp.txt', 'r')
    entrada_cabe = entrada.readline()
    CPU_Clock = int(entrada_cabe.split('|')[1])
    processos = []
    entrada_array = entrada.readlines()
    entrada_array.pop(0)
    entrada.close()
    demo_str = ''

    # Organiza os processos em listas
    for k in entrada_array:
        processos.append(k.split('|'))

    # Escalonamento

    # Tipo 1: Prioridade
    if tipo == 1:

        # Cronometro
        t_f = time.time()

        # Organiza os processos em listas por prioridade
        Processos = Priorizar(processos)

        # Auxiliar contagem de vezes que a cpu foi usada
        clock_times = 0

        # Roda as prioridades dentro da lista
        for Prioridade in Processos:
            Prioridade.pop(0)

            # Roda os processos na prioridade
            for Processo in Prioridade:

                # Recebe o tempo de cpu do processo
                pro_clock = int(Processo[2])

                # Roda enquanto o processo esta na cpu
                executando = True
                while executando:

                    # Tempo de cpu do processo subtrai a fração de cpu
                    pro_clock -= int(CPU_Clock)

                    # Contador auxiliar soma 1 a cada subtração
                    clock_times += 1
                    if pro_clock <= 0:
                        executando = False

                # Interface
                demo_str += f'Nome: {Processo[0]} |PID: {Processo[1]} |Tempo de Execução: {Processo[2]} |Prioridade: {Processo[3]} |UID: {Processo[4]} |qtdeMem: {Processo[5]}bytes |Latência: {clock_times * CPU_Clock}ms\n\n'

        # Final do cronometro
        t_f = time.time() - t_f
        prop_label.insert(1.0, f"Type: Prioridade Tipo 1 | Tempo Total: {clock_times * CPU_Clock}ms | Tempo Real: {t_f*1000:.5f}ms\n")

        # Reinicia cronometro
        t_f = time.time()

        # Organiza os processos por prioridade
        Processos2 = PriorizarOld(processos)

        # Auxiliar contagem de vezes que a cpu foi usada
        clock_times = 0

        # Roda os processos por prioridade
        for Processo in Processos2:

            # Recebe o tempo de cpu do processo
            pro_clock = int(Processo[2])

            # Roda enquanto o processo esta na cpu
            executando = True
            while executando:
                # Tempo de cpu do processo subtrai a fração de cpu
                pro_clock -= int(CPU_Clock)

                # Contador auxiliar soma 1 a cada subtração
                clock_times += 1
                if pro_clock <= 0:
                    executando = False

        # Final do cronometro
        t_f = time.time() - t_f
        prop_label.insert(1.0, f"Type: Prioridade Tipo 2 | Tempo Total: {clock_times * CPU_Clock}ms | Tempo Real: {t_f*1000:.5f}ms\n")

    # Tipo 2: Alternacia
    elif tipo == 2:

        # Cronometro
        t_f = time.time()

        # Auxiliar contagem de vezes que a cpu foi usada
        clock_times = 0

        # Contador de processos finalizados
        count_aux = 0

        # Contador de index
        i = 0

        # Enquanto os aprocessos estão sendo executados
        while 1:

            # Auxiliar contagem de vezes que a cpu foi usada
            pro_clock = int((processos[i])[2])

            # Se o processo precisa de tempo na cpu
            if pro_clock > 0:

                # Recebe o tempo de cpu do processo
                pro_clock -= int(CPU_Clock)

                # Se o processo menos a fração de cpu for menor que 0
                if pro_clock - int(CPU_Clock) < 0:
                    # Armazena a latencia final do processo no index de Tempo de processo do própio
                    pro_clock = -(clock_times*CPU_Clock)

                # cpu utilizada
                clock_times += 1

                # Atualiza o tempo de cpu do processo
                (processos[i]).pop(2)
                (processos[i]).insert(2, str(pro_clock))

                # Tira do inicio e põe no final da lista
                processos.append(processos[i])
                processos.pop()

            # Se o processo não precisa de tempo na cpu
            else:

                # Processos finalizados soma 1
                count_aux += 1

            # Se o index da lista for igual ao seu tamanho
            if i == len(processos)-1:

                # reinicia os contadores
                count_aux = 0
                i = 0

            # Se o index da lista não for igual ao seu tamanho
            else:

                # Index da lista passa para o proximo
                i += 1

            # Se o n° de proc. finalizados for igual ao n° total de processos
            if count_aux == len(processos)-1:
                # Finaliza a execução dos processos
                break

        # Inteface
        for processo in processos:
            demo_str += f'Nome: {processo[0]} |PID: {processo[1]} |Prioridade: {processo[3]} |UID: {processo[4]} |qtdeMem: {processo[5]}bytes |Latência: {-int(processo[2])}ms\n\n'
        t_f = time.time() - t_f
        prop_label.insert(1.0,
                      f"Type: Alternacia | Tempo Total: {clock_times * CPU_Clock}ms | Tempo Real: {t_f * 1000:.5f}ms\n")

    # Tipo 3: Loteria
    elif tipo == 3:

        # Cronometro
        t_f = time.time()

        # Organiza os processos em listas por prioridade
        Processos = Priorizar(processos)

        # Auxiliar contagem de vezes que a cpu foi usada
        clock_times = 0


        h = len(Processos)-1

        og2 = []

        # Enquanto os processos estão sendo organizados
        while 1:

            # A lista
            if len(Processos) >= 0:
                if len(Processos[h]) >= 0:
                    if h == 0 and len(Processos[h]) == 1:
                        break
                    elif len(Processos[h]) == 1:
                        Processos.pop()
                        h -= 1
                    else:
                        sorteado = random.randint(1, len(Processos[h])-1)
                        og2.append((Processos[h])[sorteado])
                        (Processos[h]).pop(sorteado)

        # Roda os processos por prioridade
        for Processo in og2:

            # Recebe o tempo de cpu do processo
            pro_clock = int(Processo[2])

            # Roda enquanto o processo esta na cpu
            executando = True
            while executando:

                # Tempo de cpu do processo subtrai a fração de cpu
                pro_clock -= int(CPU_Clock)

                # Contador auxiliar soma 1 a cada subtração
                clock_times += 1


                if pro_clock <= 0:
                    executando = False


            demo_str += f'Nome: {Processo[0]} |PID: {Processo[1]} |Tempo de Execução: {Processo[2]} |Prioridade: {Processo[3]} |UID: {Processo[4]} |qtdeMem: {Processo[5]}bytes |Latência: {clock_times * CPU_Clock}ms\n\n'
        t_f = time.time() - t_f
        prop_label.insert(1.0, f"Type: Loteria | Tempo Total: {clock_times * CPU_Clock}ms | Tempo Real: {t_f*1000:.5f}ms\n")

    return pos_esc.insert('1.0', demo_str)


def clear(pre_esc, pos_esc, ent_var, clock_var, prop_label):
    dirpath = os.path.dirname(__file__)
    ent_var.set('')
    clock_var.set('')
    pre_esc.delete('1.0', END)
    pos_esc.delete('1.0', END)
    prop_label.delete('1.0', END)
    os.remove(dirpath + '\\System16\\SystemData\\temp.txt')


def FileOpener(pre_esc, ent_var, clock_var, type_var, prop_label, pos_esc):

    ent_var.set('')
    clock_var.set('')
    pre_esc.delete('1.0', END)
    prop_label.delete('1.0', END)
    pos_esc.delete('1.0', END)

    dirpath = os.path.dirname(__file__)
    path = filedialog.askopenfilename(initialdir=dirpath + '\\System16\\SystemData', title="Select a File",
                                      filetypes=(("Arquivos de Texto", "*.txt*"), ("all files", "*.*")))
    entrada = open(path, 'r')
    entrada_cabe = entrada.readline()
    entrada_str = entrada.read()
    temp = open(dirpath + '\\System16\\SystemData\\temp.txt', 'w+')
    temp.write(f'{entrada_cabe}\n{entrada_str}')
    temp.close()
    clock_var.set(entrada_cabe.split('|')[1])
    type_var.set(entrada_cabe.split('|')[0])
    pre_esc.insert(1.0, entrada_str)
    ent_var.set(entrada_str)
    entrada.close()
    prop_label.insert(1.0, f"Type: {type_var.get()} | CPU_Freq: {clock_var.get()} | Processos: {len(entrada_str.splitlines())}\n")


def EntradaAleatoria(pre_esc, ent_var, clock_var, type_var, prop_label, pos_esc):

    ent_var.set('')
    clock_var.set('')
    pre_esc.delete('1.0', END)
    prop_label.delete('1.0', END)
    pos_esc.delete('1.0', END)

    GenerateProcess()
    dirpath = os.path.dirname(__file__)

    entrada = open(dirpath + '\\System16\\SystemData\\ProcessosAleatórios.txt', 'r+')
    entrada_cabe = entrada.readline()
    entrada_str = entrada.read()
    temp = open(dirpath + '\\System16\\SystemData\\temp.txt', 'w+')
    temp.write(f'{entrada_cabe}\n{entrada_str}')
    temp.close()
    clock_var.set(entrada_cabe.split('|')[1])
    type_var.set(entrada_cabe.split('|')[0])
    pre_esc.insert(1.0, entrada_str)
    ent_var.set(entrada_str)
    entrada.close()
    prop_label.insert(1.0, f"Type: {type_var.get()} | CPU_Freq: {clock_var.get()} | Processos: {len(entrada_str.splitlines())}\n")


def EscalonarWin():
    type_var = StringVar()
    clock_var = IntVar()
    ent_var = StringVar()

    EscWin = Tk()
    EscWin.geometry('600x600')
    EscWin.title('Escalonador.exe')
    EscWin.configure(background='#d4d0c7')

    file_but = Button(EscWin,
                      background='#d4d0c7',
                      text='Open File',
                      font=('Microsoft Sans Serif', 10, 'normal'),
                      command=lambda: FileOpener(pre_esc, ent_var, clock_var, type_var, prop_label, pos_esc),
                      relief="raised"
                      ).grid(column=0, row=0, pady=10)

    random_but = Button(EscWin,
                        background='#d4d0c7',
                        text='Generate',
                        font=('Microsoft Sans Serif', 10, 'normal'),
                        command=lambda: EntradaAleatoria(pre_esc, ent_var, clock_var, type_var, prop_label, pos_esc),
                        relief="raised"
                        ).grid(column=1, row=0, pady=10)

    pri_but = Button(EscWin,
                     background='#d4d0c7',
                     text='Prioridade',
                     font=('Microsoft Sans Serif', 10, 'normal'),
                     command=lambda: Escalonar(1, pos_esc, prop_label),
                     relief="raised",
                     ).grid(column=2, row=0, pady=10)

    alt_but = Button(EscWin,
                     background='#d4d0c7',
                     text='Alternacia',
                     font=('Microsoft Sans Serif', 10, 'normal'),
                     command=lambda: Escalonar(2, pos_esc, prop_label),
                     relief="raised"
                     ).grid(column=3, row=0, pady=10)

    lot_but = Button(EscWin,
                     background='#d4d0c7',
                     text='Loteria',
                     font=('Microsoft Sans Serif', 10, 'normal'),
                     command=lambda: Escalonar(3, pos_esc, prop_label),
                     relief="raised"
                     ).grid(column=4, row=0, pady=10)

    cfs_but = Button(EscWin,
                     background='#d4d0c7',
                     text='CFS',
                     font=('Microsoft Sans Serif', 10, 'normal'),
                     relief="raised"
                     ).grid(column=5, row=0, pady=10)

    clear_but = Button(EscWin,
                       background='#d4d0c7',
                       text='Clear',
                       command=lambda: clear(pre_esc, pos_esc, ent_var, clock_var, prop_label),
                       font=('Microsoft Sans Serif', 10, 'normal'),
                       relief="raised"
                       ).grid(column=6, row=0, pady=10)

    pre_esc = scrolledtext.ScrolledText(EscWin,
                                        wrap=WORD,
                                        width=25,
                                        height=25,
                                        font=('Microsoft Sans Serif', 10, 'normal'))

    pre_esc.place(x=5, y=55)

    pos_esc = scrolledtext.ScrolledText(EscWin,
                                        wrap=WORD,
                                        width=45,
                                        height=25,
                                        font=('Microsoft Sans Serif', 10, 'normal'))

    pos_esc.place(x=235, y=55)

    prop_label = scrolledtext.ScrolledText(EscWin,
                                        wrap=WORD,
                                        width=78,
                                        height=7,
                                        font=('Microsoft Sans Serif', 10, 'normal'))

    prop_label.place(x=5, y=470)

