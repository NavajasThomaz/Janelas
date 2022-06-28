import random
import os

dirpath = os.path.dirname(__file__)


def GenerateProcess(nome='Aleatório', clock=None, numProcessos=None):
    if clock is None:
        clock = random.randint(1, 10)
    if numProcessos is None:
        numProcessos = random.randint(1, 1025)
    out = open(dirpath + "\\System16\\SystemData\\ProcessosAleatórios.txt", 'w+')
    out.write(f"{nome}|{str(clock)}\n")
    for i in range(0, numProcessos):
        tempo = random.randrange(1, 10) * clock
        prioridade = random.randrange(1, 100)
        UID = random.randrange(1, 10)
        memoria = random.randrange(1, 10) * 1024
        out.write(
            "processo-" + str(i) + "|" + str(i) + "|" + str(tempo) + "|" + str(prioridade) + "|" + str(UID) + "|" + str(
                memoria) + "\n")

    out.close()
