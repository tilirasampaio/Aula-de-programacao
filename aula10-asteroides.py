import tkinter as tk
import random
import math

# =========================================================
# CONFIG
# =========================================================

LARGURA = 1200
ALTURA = 750

janela = tk.Tk()
janela.title("Mini Blox Fruits Characters Edition")

canvas = tk.Canvas(
    janela,
    width=LARGURA,
    height=ALTURA,
    bg="#6ec6ff"
)
canvas.pack()

# =========================================================
# PLAYER
# =========================================================

player = {
    "x": 500,
    "y": 350,

    "vida": 100,
    "max_vida": 100,

    "energia": 100,
    "max_energia": 100,

    "level": 1,
    "xp": 0,

    "dano": 20,

    "money": 0,

    "fruta": "fogo",

    "kills": 0
}

# =========================================================
# COOLDOWN ESPADA
# =========================================================

cooldown_espada = 0
cooldown_max_espada = 20

# =========================================================
# QUEST
# =========================================================

quest = {
    "nome": "Derrote 10 inimigos",
    "progresso": 0,
    "objetivo": 10,
    "recompensa": 200,
    "completa": False
}

# =========================================================
# NPCS
# =========================================================

npcs = [
    {
        "x": 250,
        "y": 470,
        "nome": "Bandit Quest",
        "fala": "Derrote 10 inimigos!"
    },

    {
        "x": 650,
        "y": 450,
        "nome": "Fruit Master",
        "fala": "Use F para poderes!"
    },

    {
        "x": 1000,
        "y": 480,
        "nome": "Sword Dealer",
        "fala": "Sua espada esta forte!"
    }
]

# =========================================================
# INIMIGOS
# =========================================================

inimigos = []

def criar_inimigo():

    return {
        "x": random.randint(50, 1150),
        "y": random.randint(50, 650),

        "vida": 50,
        "max_vida": 50,

        "vel": random.uniform(1, 2),

        "boss": False
    }

def criar_boss():

    return {
        "x": random.randint(200, 1000),
        "y": random.randint(100, 500),

        "vida": 400,
        "max_vida": 400,

        "vel": 0.8,

        "boss": True
    }

for _ in range(8):
    inimigos.append(criar_inimigo())

# =========================================================
# ILHAS
# =========================================================

ilhas = [
    {"x": 150, "y": 520},
    {"x": 550, "y": 500},
    {"x": 950, "y": 530},
]

# =========================================================
# CONTROLES
# =========================================================

teclas = set()

def tecla_press(event):

    teclas.add(event.keysym)

    if event.keysym == "space":
        atacar_espada()

    if event.keysym.lower() == "f":
        poder_fruta()

def tecla_release(event):
    teclas.discard(event.keysym)

janela.bind("<KeyPress>", tecla_press)
janela.bind("<KeyRelease>", tecla_release)

# =========================================================
# XP
# =========================================================

def ganhar_xp(valor):

    player["xp"] += valor

    xp_necessario = player["level"] * 50

    while player["xp"] >= xp_necessario:

        player["xp"] -= xp_necessario

        player["level"] += 1

        player["max_vida"] += 20
        player["vida"] = player["max_vida"]

        player["dano"] += 5

        xp_necessario = player["level"] * 50

# =========================================================
# EFEITOS
# =========================================================

efeitos = []

# =========================================================
# ESPADA
# =========================================================

def atacar_espada():

    global cooldown_espada

    if cooldown_espada > 0:
        return

    cooldown_espada = cooldown_max_espada

    efeitos.append({
        "tipo": "espada",
        "tempo": 10
    })

    for inimigo in inimigos[:]:

        dist = math.hypot(
            inimigo["x"] - player["x"],
            inimigo["y"] - player["y"]
        )

        if dist < 80:

            inimigo["vida"] -= player["dano"]

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# PODER FRUTA
# =========================================================

def poder_fruta():

    if player["energia"] < 30:
        return

    player["energia"] -= 30

    efeitos.append({
        "tipo": "fruta",
        "tempo": 20
    })

    for inimigo in inimigos[:]:

        dist = math.hypot(
            inimigo["x"] - player["x"],
            inimigo["y"] - player["y"]
        )

        if dist < 180:

            dano = player["dano"] * 2

            inimigo["vida"] -= dano

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# MATAR INIMIGO
# =========================================================

def matar_inimigo(inimigo):

    if inimigo in inimigos:
        inimigos.remove(inimigo)

    if inimigo["boss"]:

        ganhar_xp(250)
        player["money"] += 500

    else:

        ganhar_xp(25)
        player["money"] += random.randint(10, 30)

    player["kills"] += 1

    if not quest["completa"]:

        quest["progresso"] += 1

        if quest["progresso"] >= quest["objetivo"]:

            quest["completa"] = True
            player["money"] += quest["recompensa"]

# =========================================================
# DESENHAR PERSONAGEM
# =========================================================

def desenhar_personagem(x, y, cor_roupa, nome=None):

    # pernas
    canvas.create_line(
        x - 8, y + 20,
        x - 12, y + 35,
        width=4,
        fill="black"
    )

    canvas.create_line(
        x + 8, y + 20,
        x + 12, y + 35,
        width=4,
        fill="black"
    )

    # corpo
    canvas.create_rectangle(
        x - 12,
        y - 5,

        x + 12,
        y + 20,

        fill=cor_roupa,
        outline="black"
    )

    # braços
    canvas.create_line(
        x - 12, y,
        x - 25, y + 10,
        width=4
    )

    canvas.create_line(
        x + 12, y,
        x + 25, y + 10,
        width=4
    )

    # cabeça
    canvas.create_oval(
        x - 12,
        y - 30,

        x + 12,
        y - 5,

        fill="#f1c27d",
        outline="black"
    )

    # cabelo
    canvas.create_arc(
        x - 13,
        y - 32,

        x + 13,
        y - 10,

        start=0,
        extent=180,

        fill="black",
        outline="black"
    )

    # olhos
    canvas.create_oval(
        x - 6,
        y - 22,

        x - 2,
        y - 18,

        fill="black"
    )

    canvas.create_oval(
        x + 2,
        y - 22,

        x + 6,
        y - 18,

        fill="black"
    )

    # boca
    canvas.create_line(
        x - 4,
        y - 12,

        x + 4,
        y - 12,

        fill="black"
    )

    if nome:

        canvas.create_text(
            x,
            y - 45,

            text=nome,
            fill="white",

            font=("Arial", 10, "bold")
        )

# =========================================================
# UPDATE
# =========================================================

boss_spawnado = False

def atualizar():

    global boss_spawnado
    global cooldown_espada

    # =====================================================
    # MOVIMENTO
    # =====================================================

    velocidade = 5

    if "Shift_L" in teclas:
        velocidade = 10

    if "Left" in teclas:
        player["x"] -= velocidade

    if "Right" in teclas:
        player["x"] += velocidade

    if "Up" in teclas:
        player["y"] -= velocidade

    if "Down" in teclas:
        player["y"] += velocidade

    player["x"] = max(20, min(LARGURA - 20, player["x"]))
    player["y"] = max(20, min(ALTURA - 20, player["y"]))

    # =====================================================
    # ENERGIA
    # =====================================================

    if player["energia"] < player["max_energia"]:

        player["energia"] += 0.3

        player["energia"] = min(
            player["energia"],
            player["max_energia"]
        )

    # =====================================================
    # COOLDOWN
    # =====================================================

    if cooldown_espada > 0:
        cooldown_espada -= 1

    # =====================================================
    # IA INIMIGOS
    # =====================================================

    for inimigo in inimigos:

        dx = player["x"] - inimigo["x"]
        dy = player["y"] - inimigo["y"]

        dist = math.hypot(dx, dy)

        if dist > 0:

            inimigo["x"] += (dx / dist) * inimigo["vel"]
            inimigo["y"] += (dy / dist) * inimigo["vel"]

        if dist < 30:

            if inimigo["boss"]:
                player["vida"] -= 0.4
            else:
                player["vida"] -= 0.1

    # =====================================================
    # RESPAWN
    # =====================================================

    while len([i for i in inimigos if not i["boss"]]) < 8:
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
        0, 0,
        LARGURA, ALTURA,
        fill="#6ec6ff",
        outline=""
    )

    # água
    canvas.create_rectangle(
        0, 600,
        LARGURA, ALTURA,
        fill="#1f75fe",
        outline=""
    )

    # ilhas
    for ilha in ilhas:

        canvas.create_oval(
            ilha["x"] - 120,
            ilha["y"] - 40,

            ilha["x"] + 120,
            ilha["y"] + 40,

            fill="#9c6b30",
            outline=""
        )

        canvas.create_rectangle(
            ilha["x"] - 120,
            ilha["y"],

            ilha["x"] + 120,
            ilha["y"] + 40,

            fill="#3cb043",
            outline=""
        )

    # =====================================================
    # NPCS
    # =====================================================

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

        if dist < 90:

            canvas.create_text(
                npc["x"],
                npc["y"] - 65,

                text=npc["fala"],
                fill="yellow",

                font=("Arial", 10, "bold")
            )

    # =====================================================
    # PLAYER
    # =====================================================

    desenhar_personagem(
        player["x"],
        player["y"],
        "blue",
        f"Lv {player['level']}"
    )

    # espada
    canvas.create_line(
        player["x"] + 20,
        player["y"],

        player["x"] + 40,
        player["y"] - 20,

        width=5,
        fill="silver"
    )

    # =====================================================
    # EFEITOS
    # =====================================================

    for efeito in efeitos[:]:

        if efeito["tipo"] == "espada":

            canvas.create_oval(
                player["x"] - 80,
                player["y"] - 80,

                player["x"] + 80,
                player["y"] + 80,

                outline="white",
                width=4
            )

        elif efeito["tipo"] == "fruta":

            canvas.create_oval(
                player["x"] - 180,
                player["y"] - 180,

                player["x"] + 180,
                player["y"] + 180,

                outline="orange",
                width=6
            )

        efeito["tempo"] -= 1

        if efeito["tempo"] <= 0:
            efeitos.remove(efeito)

    # =====================================================
    # INIMIGOS
    # =====================================================

    for inimigo in inimigos:

        cor = "purple" if inimigo["boss"] else "red"

        nome = "BOSS" if inimigo["boss"] else "Bandit"

        desenhar_personagem(
            inimigo["x"],
            inimigo["y"],
            cor,
            nome
        )

        # barra vida
        canvas.create_rectangle(
            inimigo["x"] - 20,
            inimigo["y"] - 55,

            inimigo["x"] + 20,
            inimigo["y"] - 48,

            fill="gray"
        )

        vida = (
            inimigo["vida"] /
            inimigo["max_vida"]
        ) * 40

        canvas.create_rectangle(
            inimigo["x"] - 20,
            inimigo["y"] - 55,

            inimigo["x"] - 20 + vida,
            inimigo["y"] - 48,

            fill="lime"
        )

    # =====================================================
    # HUD
    # =====================================================

    # VIDA
    canvas.create_text(
        120, 20,
        text="VIDA",
        font=("Arial", 12, "bold")
    )

    canvas.create_rectangle(
        20, 30,
        220, 50,
        fill="gray"
    )

    vida_barra = (
        player["vida"] /
        player["max_vida"]
    ) * 200

    canvas.create_rectangle(
        20, 30,
        20 + vida_barra,
        50,
        fill="red"
    )

    # ENERGIA
    canvas.create_text(
        120, 70,
        text="ENERGIA",
        font=("Arial", 12, "bold")
    )

    canvas.create_rectangle(
        20, 80,
        220, 100,
        fill="gray"
    )

    energia_barra = (
        player["energia"] /
        player["max_energia"]
    ) * 200

    canvas.create_rectangle(
        20, 80,
        20 + energia_barra,
        100,
        fill="cyan"
    )

    # ESPADA CD
    canvas.create_text(
        120, 120,
        text="ESPADA",
        font=("Arial", 12, "bold")
    )

    canvas.create_rectangle(
        20, 130,
        220, 150,
        fill="gray"
    )

    largura_cd = (
        1 - (cooldown_espada / cooldown_max_espada)
    ) * 200

    canvas.create_rectangle(
        20, 130,
        20 + largura_cd,
        150,
        fill="white"
    )

    # XP
    canvas.create_text(
        120, 170,
        text=f"LEVEL {player['level']}",
        font=("Arial", 12, "bold")
    )

    canvas.create_rectangle(
        20, 180,
        220, 200,
        fill="gray"
    )

    xp_necessario = player["level"] * 50

    xp_barra = (
        player["xp"] /
        xp_necessario
    ) * 200

    canvas.create_rectangle(
        20, 180,
        20 + xp_barra,
        200,
        fill="yellow"
    )

    # dinheiro
    canvas.create_text(
        120, 240,
        text=f"$ {player['money']}",
        fill="green",

        font=("Arial", 15, "bold")
    )

    # kills
    canvas.create_text(
        120, 270,
        text=f"KILLS: {player['kills']}",
        fill="white",

        font=("Arial", 12, "bold")
    )

    # quest
    status = (
        "COMPLETA"
        if quest["completa"]
        else f"{quest['progresso']}/{quest['objetivo']}"
    )

    canvas.create_text(
        950, 30,
        text=f"QUEST: {quest['nome']}",
        font=("Arial", 12, "bold")
    )

    canvas.create_text(
        950, 60,
        text=status,
        fill="yellow",
        font=("Arial", 12, "bold")
    )

    # controles
    canvas.create_text(
        980, 130,
        text="SETAS = mover",
        font=("Arial", 12, "bold")
    )

    canvas.create_text(
        980, 160,
        text="SHIFT = dash",
        font=("Arial", 12, "bold")
    )

    canvas.create_text(
        980, 190,
        text="ESPAÇO = espada",
        font=("Arial", 12, "bold")
    )

    canvas.create_text(
        980, 220,
        text="F = fruta",
        font=("Arial", 12, "bold")
    )

    # =====================================================
    # GAME OVER
    # =====================================================

    if player["vida"] <= 0:

        canvas.create_text(
            LARGURA // 2,
            ALTURA // 2,

            text="GAME OVER",
            fill="red",

            font=("Arial", 60, "bold")
        )

        return

    janela.after(16, atualizar)

# =========================================================
# START
# =========================================================

atualizar()

janela.mainloop()