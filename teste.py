import tkinter as tk
import random
import math

# =========================================================
# CONFIG
# =========================================================

LARGURA = 1400
ALTURA = 800

janela = tk.Tk()
janela.title("Blox Fruits Ultimate Edition")

janela.resizable(False, False)
janela.focus_force()

canvas = tk.Canvas(
    janela,
    width=LARGURA,
    height=ALTURA,
    bg="#6ec6ff",
    highlightthickness=0
)
canvas.pack()

# =========================================================
# PLAYER
# =========================================================

player = {
    "x": 400,
    "y": 300,

    "vida": 100,
    "max_vida": 100,

    "energia": 100,
    "max_energia": 100,

    "level": 1,
    "xp": 0,

    "dano": 20,

    "money": 0,

    "fruta": "Fire",

    "kills": 0,

    "dash": 0,

    "haki": False,

    "transformado": False
}

# =========================================================
# INVENTARIO
# =========================================================

inventario = [
    "Katana",
    "Fire Fruit"
]

# =========================================================
# QUEST
# =========================================================

quest = {
    "nome": "Derrote 15 inimigos",
    "progresso": 0,
    "objetivo": 15,
    "recompensa": 500,
    "completa": False
}

# =========================================================
# EFEITOS
# =========================================================

efeitos = []

# =========================================================
# NPCS
# =========================================================

npcs = [
    {
        "x": 250,
        "y": 500,
        "nome": "Quest NPC",
        "fala": "Derrote inimigos!"
    },

    {
        "x": 700,
        "y": 500,
        "nome": "Haki Master",
        "fala": "Pressione H!"
    },

    {
        "x": 1150,
        "y": 500,
        "nome": "Boat Dealer",
        "fala": "Pegue um barco!"
    }
]

# =========================================================
# ILHAS
# =========================================================

ilhas = [
    {"x": 200, "y": 560, "cor": "#3cb043"},
    {"x": 700, "y": 530, "cor": "#2faa35"},
    {"x": 1200, "y": 560, "cor": "#46b94d"},
]

# =========================================================
# BARCO
# =========================================================

barco = {
    "ativo": False,
    "x": 0,
    "y": 0
}

# =========================================================
# INIMIGOS
# =========================================================

inimigos = []

def criar_inimigo():

    return {

        "x": random.randint(50, 1300),
        "y": random.randint(50, 650),

        "vida": 60,
        "max_vida": 60,

        "vel": random.uniform(1, 2),

        "boss": False
    }

def criar_boss():

    return {

        "x": random.randint(300, 1100),
        "y": random.randint(100, 500),

        "vida": 500,
        "max_vida": 500,

        "vel": 0.8,

        "boss": True
    }

for _ in range(10):
    inimigos.append(criar_inimigo())

boss_spawnado = False

# =========================================================
# CONTROLES
# =========================================================

teclas = set()

def tecla_press(event):

    teclas.add(event.keysym)

    if event.keysym == "space":
        atacar()

    if event.keysym.lower() == "f":
        poder_fruta()

    if event.keysym.lower() == "h":
        ativar_haki()

    if event.keysym.lower() == "t":
        transformar()

    if event.keysym.lower() == "b":
        spawnar_barco()

def tecla_release(event):
    teclas.discard(event.keysym)

janela.bind("<KeyPress>", tecla_press)
janela.bind("<KeyRelease>", tecla_release)

# =========================================================
# LEVEL
# =========================================================

def ganhar_xp(valor):

    player["xp"] += valor

    necessario = player["level"] * 60

    while player["xp"] >= necessario:

        player["xp"] -= necessario

        player["level"] += 1

        player["max_vida"] += 20
        player["vida"] = player["max_vida"]

        player["dano"] += 5

        necessario = player["level"] * 60

# =========================================================
# ATAQUE
# =========================================================

def atacar():

    efeitos.append({
        "tipo": "espada",
        "tempo": 8
    })

    dano = player["dano"]

    if player["haki"]:
        dano *= 2

    for inimigo in inimigos[:]:

        dist = math.hypot(
            inimigo["x"] - player["x"],
            inimigo["y"] - player["y"]
        )

        if dist < 100:

            inimigo["vida"] -= dano

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# FRUTA
# =========================================================

def poder_fruta():

    if player["energia"] < 25:
        return

    player["energia"] -= 25

    efeitos.append({
        "tipo": "fogo",
        "tempo": 15
    })

    for inimigo in inimigos[:]:

        dist = math.hypot(
            inimigo["x"] - player["x"],
            inimigo["y"] - player["y"]
        )

        if dist < 200:

            inimigo["vida"] -= player["dano"] * 2

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# HAKI
# =========================================================

def ativar_haki():

    player["haki"] = not player["haki"]

# =========================================================
# TRANSFORMAÇÃO
# =========================================================

def transformar():

    if player["level"] < 5:
        return

    player["transformado"] = not player["transformado"]

# =========================================================
# BARCO
# =========================================================

def spawnar_barco():

    barco["ativo"] = True

    barco["x"] = player["x"]
    barco["y"] = 650

# =========================================================
# MORTE
# =========================================================

def matar_inimigo(inimigo):

    if inimigo in inimigos:
        inimigos.remove(inimigo)

    if inimigo["boss"]:

        ganhar_xp(300)
        player["money"] += 800

    else:

        ganhar_xp(30)
        player["money"] += random.randint(20, 40)

    player["kills"] += 1

    if not quest["completa"]:

        quest["progresso"] += 1

        if quest["progresso"] >= quest["objetivo"]:

            quest["completa"] = True
            player["money"] += quest["recompensa"]

# =========================================================
# PERSONAGEM
# =========================================================

def desenhar_personagem(x, y, cor, nome=None):

    brilho = "yellow" if player["transformado"] else cor

    # pernas
    canvas.create_line(x-8,y+20,x-12,y+35,width=4)
    canvas.create_line(x+8,y+20,x+12,y+35,width=4)

    # corpo
    canvas.create_rectangle(
        x-12,y-5,
        x+12,y+20,
        fill=brilho,
        outline="black"
    )

    # braços
    canvas.create_line(x-12,y,x-25,y+10,width=4)
    canvas.create_line(x+12,y,x+25,y+10,width=4)

    # cabeça
    canvas.create_oval(
        x-12,y-30,
        x+12,y-5,
        fill="#f1c27d"
    )

    # cabelo anime
    canvas.create_polygon(
        x-12,y-18,
        x-6,y-35,
        x,y-22,
        x+6,y-35,
        x+12,y-18,
        fill="black"
    )

    # haki aura
    if player["haki"]:

        canvas.create_oval(
            x-30,y-45,
            x+30,y+40,
            outline="black",
            width=3
        )

    if nome:

        canvas.create_text(
            x,
            y-50,
            text=nome,
            fill="white",
            font=("Arial",10,"bold")
        )

# =========================================================
# UPDATE
# =========================================================

def atualizar():

    global boss_spawnado

    velocidade = 5

    if "Shift_L" in teclas:
        velocidade = 10

    if player["transformado"]:
        velocidade = 8

    if "Left" in teclas:
        player["x"] -= velocidade

    if "Right" in teclas:
        player["x"] += velocidade

    if "Up" in teclas:
        player["y"] -= velocidade

    if "Down" in teclas:
        player["y"] += velocidade

    player["x"] = max(20, min(LARGURA-20, player["x"]))
    player["y"] = max(20, min(ALTURA-20, player["y"]))

    # energia
    if player["energia"] < player["max_energia"]:
        player["energia"] += 0.4

    # inimigos
    for inimigo in inimigos:

        dx = player["x"] - inimigo["x"]
        dy = player["y"] - inimigo["y"]

        dist = math.hypot(dx,dy)

        if dist > 0:

            inimigo["x"] += (dx/dist) * inimigo["vel"]
            inimigo["y"] += (dy/dist) * inimigo["vel"]

        if dist < 30:

            if inimigo["boss"]:
                player["vida"] -= 0.5
            else:
                player["vida"] -= 0.15

    # respawn
    while len([i for i in inimigos if not i["boss"]]) < 10:
        inimigos.append(criar_inimigo())

    if player["level"] >= 5 and not boss_spawnado:

        inimigos.append(criar_boss())
        boss_spawnado = True

    # =====================================================
    # DESENHO
    # =====================================================

    canvas.delete("all")

    # céu
    canvas.create_rectangle(
        0,0,
        LARGURA,ALTURA,
        fill="#6ec6ff",
        outline=""
    )

    # sol
    canvas.create_oval(
        50,50,
        150,150,
        fill="yellow",
        outline=""
    )

    # água
    canvas.create_rectangle(
        0,620,
        LARGURA,ALTURA,
        fill="#1f75fe",
        outline=""
    )

    # ondas
    for i in range(0,LARGURA,40):

        canvas.create_arc(
            i,620,
            i+40,650,
            start=0,
            extent=180,
            style="arc",
            width=2
        )

    # ilhas
    for ilha in ilhas:

        canvas.create_oval(
            ilha["x"]-130,
            ilha["y"]-40,

            ilha["x"]+130,
            ilha["y"]+40,

            fill="#9c6b30",
            outline=""
        )

        canvas.create_rectangle(
            ilha["x"]-130,
            ilha["y"],

            ilha["x"]+130,
            ilha["y"]+40,

            fill=ilha["cor"],
            outline=""
        )

        # palmeira
        canvas.create_line(
            ilha["x"],
            ilha["y"]-60,

            ilha["x"],
            ilha["y"],

            width=10,
            fill="#8b5a2b"
        )

        canvas.create_oval(
            ilha["x"]-30,
            ilha["y"]-90,

            ilha["x"]+30,
            ilha["y"]-40,

            fill="green"
        )

    # barco
    if barco["ativo"]:

        canvas.create_rectangle(
            barco["x"]-40,
            barco["y"]-10,

            barco["x"]+40,
            barco["y"]+10,

            fill="#8b5a2b"
        )

        canvas.create_line(
            barco["x"],
            barco["y"]-50,

            barco["x"],
            barco["y"]-10,

            width=4
        )

        canvas.create_polygon(
            barco["x"],
            barco["y"]-50,

            barco["x"],
            barco["y"]-20,

            barco["x"]+30,
            barco["y"]-35,

            fill="white"
        )

    # npcs
    for npc in npcs:

        desenhar_personagem(
            npc["x"],
            npc["y"],
            "#8b5a2b",
            npc["nome"]
        )

        dist = math.hypot(
            player["x"] - npc["x"],
            player["y"] - npc["y"]
        )

        if dist < 100:

            canvas.create_text(
                npc["x"],
                npc["y"]-70,
                text=npc["fala"],
                fill="yellow",
                font=("Arial",10,"bold")
            )

    # player
    cor_player = "orange" if player["transformado"] else "blue"

    desenhar_personagem(
        player["x"],
        player["y"],
        cor_player,
        f"Lv {player['level']}"
    )

    # espada
    canvas.create_line(
        player["x"]+20,
        player["y"],

        player["x"]+45,
        player["y"]-25,

        width=5,
        fill="silver"
    )

    # efeitos
    for efeito in efeitos[:]:

        if efeito["tipo"] == "espada":

            canvas.create_oval(
                player["x"]-100,
                player["y"]-100,

                player["x"]+100,
                player["y"]+100,

                outline="white",
                width=4
            )

        if efeito["tipo"] == "fogo":

            canvas.create_oval(
                player["x"]-200,
                player["y"]-200,

                player["x"]+200,
                player["y"]+200,

                outline="orange",
                width=6
            )

        efeito["tempo"] -= 1

        if efeito["tempo"] <= 0:
            efeitos.remove(efeito)

    # inimigos
    for inimigo in inimigos:

        cor = "purple" if inimigo["boss"] else "red"

        nome = "BOSS" if inimigo["boss"] else "Bandit"

        desenhar_personagem(
            inimigo["x"],
            inimigo["y"],
            cor,
            nome
        )

        # vida
        canvas.create_rectangle(
            inimigo["x"]-25,
            inimigo["y"]-55,

            inimigo["x"]+25,
            inimigo["y"]-48,

            fill="gray"
        )

        vida = (
            inimigo["vida"] /
            inimigo["max_vida"]
        ) * 50

        canvas.create_rectangle(
            inimigo["x"]-25,
            inimigo["y"]-55,

            inimigo["x"]-25+vida,
            inimigo["y"]-48,

            fill="lime"
        )

    # HUD
    canvas.create_text(
        120,20,
        text=f"VIDA {int(player['vida'])}",
        font=("Arial",12,"bold")
    )

    canvas.create_rectangle(
        20,30,
        220,50,
        fill="gray"
    )

    vida_barra = (
        player["vida"] /
        player["max_vida"]
    ) * 200

    canvas.create_rectangle(
        20,30,
        20+vida_barra,50,
        fill="red"
    )

    # energia
    canvas.create_text(
        120,70,
        text="ENERGIA",
        font=("Arial",12,"bold")
    )

    canvas.create_rectangle(
        20,80,
        220,100,
        fill="gray"
    )

    energia = (
        player["energia"] /
        player["max_energia"]
    ) * 200

    canvas.create_rectangle(
        20,80,
        20+energia,100,
        fill="cyan"
    )

    # xp
    xp_need = player["level"] * 60

    xp_bar = (
        player["xp"] /
        xp_need
    ) * 200

    canvas.create_text(
        120,120,
        text=f"LEVEL {player['level']}",
        font=("Arial",12,"bold")
    )

    canvas.create_rectangle(
        20,130,
        220,150,
        fill="gray"
    )

    canvas.create_rectangle(
        20,130,
        20+xp_bar,150,
        fill="yellow"
    )

    # dinheiro
    canvas.create_text(
        120,190,
        text=f"$ {player['money']}",
        fill="green",
        font=("Arial",16,"bold")
    )

    # kills
    canvas.create_text(
        120,220,
        text=f"KILLS {player['kills']}",
        fill="white",
        font=("Arial",12,"bold")
    )

    # quest
    status = (
        "COMPLETA"
        if quest["completa"]
        else f"{quest['progresso']}/{quest['objetivo']}"
    )

    canvas.create_text(
        1100,20,
        text=quest["nome"],
        font=("Arial",12,"bold")
    )

    canvas.create_text(
        1100,50,
        text=status,
        fill="yellow",
        font=("Arial",12,"bold")
    )

    # inventário
    canvas.create_text(
        1100,100,
        text="INVENTARIO",
        font=("Arial",12,"bold")
    )

    y_inv = 130

    for item in inventario:

        canvas.create_text(
            1100,y_inv,
            text=f"- {item}",
            fill="white",
            font=("Arial",10,"bold")
        )

        y_inv += 25

    # controles
    controles = [
        "SETAS = mover",
        "SHIFT = dash",
        "SPACE = espada",
        "F = fruta",
        "H = haki",
        "T = transformação",
        "B = barco"
    ]

    y_txt = 300

    for c in controles:

        canvas.create_text(
            1150,
            y_txt,
            text=c,
            font=("Arial",11,"bold")
        )

        y_txt += 30

    # game over
    if player["vida"] <= 0:

        canvas.create_text(
            LARGURA//2,
            ALTURA//2,

            text="GAME OVER",

            fill="red",
            font=("Arial",70,"bold")
        )

        return

    janela.after(16, atualizar)

# =========================================================
# START
# =========================================================

atualizar()

janela.mainloop()