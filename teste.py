# =========================================================
# MINI BLOX FRUITS - COM SISTEMA DE FRUTAS
# =========================================================

import tkinter as tk
import random
import math

# =========================================================
# JANELA
# =========================================================

LARGURA = 1280
ALTURA = 720

MAPA_LARGURA = 4000
MAPA_ALTURA = 2500

janela = tk.Tk()
janela.title("Mini Blox Fruits Fruits Update")

canvas = tk.Canvas(
    janela,
    width=LARGURA,
    height=ALTURA,
    bg="#6ec6ff",
    highlightthickness=0
)

canvas.pack()

# =========================================================
# CAMERA
# =========================================================

camera_x = 0
camera_y = 0

# =========================================================
# PLAYER
# =========================================================

player = {
    "x": 800,
    "y": 700,

    "vida": 100,
    "max_vida": 100,

    "energia": 100,
    "max_energia": 100,

    "level": 1,
    "xp": 0,

    "money": 0,

    "dano": 20,

    "kills": 0,

    "vel": 5,

    "fruta": "Fogo",

    "espada": "Katana",

    "transformado": False
}

# =========================================================
# FRUTAS
# =========================================================

frutas = {

    "Fogo": {
        "cor": "orange",
        "dano": 2,
        "energia": 30,
        "raio": 240,
        "efeito": "burn"
    },

    "Gelo": {
        "cor": "cyan",
        "dano": 1.5,
        "energia": 25,
        "raio": 220,
        "efeito": "slow"
    },

    "Luz": {
        "cor": "yellow",
        "dano": 2.5,
        "energia": 35,
        "raio": 300,
        "efeito": "flash"
    },

    "Magma": {
        "cor": "red",
        "dano": 3,
        "energia": 40,
        "raio": 200,
        "efeito": "explode"
    },

    "Trevas": {
        "cor": "purple",
        "dano": 2.2,
        "energia": 35,
        "raio": 260,
        "efeito": "pull"
    }
}

# =========================================================
# FRUTAS SPAWNADAS
# =========================================================

frutas_spawnadas = []

def spawnar_fruta():

    nome = random.choice(list(frutas.keys()))

    frutas_spawnadas.append({

        "x": random.randint(300, MAPA_LARGURA - 300),
        "y": random.randint(300, MAPA_ALTURA - 300),

        "nome": nome,

        "tempo": 1800
    })

for _ in range(4):
    spawnar_fruta()

# =========================================================
# EFEITOS
# =========================================================

efeitos = []
particulas = []

# =========================================================
# ILHAS
# =========================================================

ilhas = [
    {"x": 700, "y": 800, "r": 220},
    {"x": 1800, "y": 600, "r": 260},
    {"x": 3000, "y": 1200, "r": 300},
]

# =========================================================
# NPCS
# =========================================================

npcs = [

    {
        "x": 1800,
        "y": 600,
        "nome": "Fruit Master",
        "fala": "Pegue frutas pelo mapa!"
    }
]

# =========================================================
# INIMIGOS
# =========================================================

inimigos = []

def criar_inimigo():

    return {

        "x": random.randint(200, 3800),
        "y": random.randint(200, 2200),

        "vida": 70,
        "max_vida": 70,

        "vel": random.uniform(1.5, 2.5),

        "boss": False,

        "hit": 0,

        "queimando": 0,
        "slow": 0,
        "flash": 0
    }

for _ in range(12):
    inimigos.append(criar_inimigo())

# =========================================================
# TECLAS
# =========================================================

teclas = set()

cooldown_espada = 0
cooldown_fruta = 0

def tecla_press(event):

    teclas.add(event.keysym)

    if event.keysym == "space":
        atacar()

    if event.keysym.lower() == "f":
        usar_fruta()

def tecla_release(event):

    if event.keysym in teclas:
        teclas.remove(event.keysym)

janela.bind("<KeyPress>", tecla_press)
janela.bind("<KeyRelease>", tecla_release)

# =========================================================
# XP
# =========================================================

def ganhar_xp(valor):

    player["xp"] += valor

    while player["xp"] >= player["level"] * 60:

        player["xp"] -= player["level"] * 60

        player["level"] += 1

        player["max_vida"] += 20
        player["vida"] = player["max_vida"]

        player["dano"] += 5

# =========================================================
# PARTICULAS
# =========================================================

def criar_particulas(x, y, cor):

    for _ in range(10):

        particulas.append({

            "x": x,
            "y": y,

            "dx": random.uniform(-4, 4),
            "dy": random.uniform(-4, 4),

            "vida": random.randint(10, 25),

            "cor": cor
        })

# =========================================================
# PEGAR FRUTA
# =========================================================

def verificar_frutas():

    for fruta in frutas_spawnadas[:]:

        dist = math.hypot(
            fruta["x"] - player["x"],
            fruta["y"] - player["y"]
        )

        if dist < 50:

            player["fruta"] = fruta["nome"]

            criar_particulas(
                fruta["x"],
                fruta["y"],
                frutas[fruta["nome"]]["cor"]
            )

            frutas_spawnadas.remove(fruta)

# =========================================================
# ATAQUE
# =========================================================

def atacar():

    global cooldown_espada

    if cooldown_espada > 0:
        return

    cooldown_espada = 12

    efeitos.append({

        "tipo": "slash",
        "tempo": 8
    })

    for inimigo in inimigos[:]:

        dx = inimigo["x"] - player["x"]
        dy = inimigo["y"] - player["y"]

        dist = math.hypot(dx, dy)

        if dist < 100:

            inimigo["vida"] -= player["dano"]

            inimigo["hit"] = 5

            criar_particulas(
                inimigo["x"],
                inimigo["y"],
                "red"
            )

            if dist != 0:

                inimigo["x"] += (dx / dist) * 40
                inimigo["y"] += (dy / dist) * 40

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# FRUTA
# =========================================================

def usar_fruta():

    global cooldown_fruta

    fruta_nome = player["fruta"]

    info = frutas[fruta_nome]

    if cooldown_fruta > 0:
        return

    if player["energia"] < info["energia"]:
        return

    player["energia"] -= info["energia"]

    cooldown_fruta = 45

    efeitos.append({

        "tipo": "fruta",
        "tempo": 18,

        "cor": info["cor"],
        "raio": info["raio"]
    })

    for inimigo in inimigos[:]:

        dx = inimigo["x"] - player["x"]
        dy = inimigo["y"] - player["y"]

        dist = math.hypot(dx, dy)

        if dist < info["raio"]:

            dano = player["dano"] * info["dano"]

            inimigo["vida"] -= dano

            inimigo["hit"] = 8

            criar_particulas(
                inimigo["x"],
                inimigo["y"],
                info["cor"]
            )

            efeito = info["efeito"]

            # fogo
            if efeito == "burn":
                inimigo["queimando"] = 120

            # gelo
            elif efeito == "slow":
                inimigo["slow"] = 180

            # luz
            elif efeito == "flash":
                inimigo["flash"] = 60

            # magma
            elif efeito == "explode":

                inimigo["vida"] -= 20

                criar_particulas(
                    inimigo["x"],
                    inimigo["y"],
                    "red"
                )

            # trevas
            elif efeito == "pull":

                if dist != 0:

                    inimigo["x"] -= (dx / dist) * 80
                    inimigo["y"] -= (dy / dist) * 80

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# MATAR
# =========================================================

def matar_inimigo(inimigo):

    if inimigo in inimigos:
        inimigos.remove(inimigo)

    ganhar_xp(25)

    player["money"] += random.randint(15, 40)

    player["kills"] += 1

# =========================================================
# PERSONAGEM
# =========================================================

def desenhar_personagem(x, y, cor, nome=None, hit=0):

    x -= camera_x
    y -= camera_y

    if hit > 0:
        cor = "white"

    # aura fruta
    fruta_cor = frutas[player["fruta"]]["cor"]

    if cor == "blue":

        canvas.create_oval(
            x - 35,
            y - 55,

            x + 35,
            y + 45,

            outline=fruta_cor,
            width=3
        )

    # pernas
    canvas.create_line(
        x - 8, y + 20,
        x - 12, y + 35,
        width=4
    )

    canvas.create_line(
        x + 8, y + 20,
        x + 12, y + 35,
        width=4
    )

    # corpo
    canvas.create_rectangle(
        x - 12,
        y - 5,

        x + 12,
        y + 20,

        fill=cor
    )

    # braços
    canvas.create_line(
        x - 12, y,
        x - 24, y + 10,
        width=4
    )

    canvas.create_line(
        x + 12, y,
        x + 24, y + 10,
        width=4
    )

    # cabeça
    canvas.create_oval(
        x - 12,
        y - 30,

        x + 12,
        y - 5,

        fill="#f1c27d"
    )

    # cabelo
    canvas.create_arc(
        x - 13,
        y - 32,

        x + 13,
        y - 12,

        start=0,
        extent=180,

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

def atualizar():

    global camera_x
    global camera_y

    global cooldown_espada
    global cooldown_fruta

    velocidade = player["vel"]

    # movimento
    if "Left" in teclas:
        player["x"] -= velocidade

    if "Right" in teclas:
        player["x"] += velocidade

    if "Up" in teclas:
        player["y"] -= velocidade

    if "Down" in teclas:
        player["y"] += velocidade

    player["x"] = max(0, min(MAPA_LARGURA, player["x"]))
    player["y"] = max(0, min(MAPA_ALTURA, player["y"]))

    # camera
    camera_x += (
        (player["x"] - LARGURA // 2) - camera_x
    ) * 0.08

    camera_y += (
        (player["y"] - ALTURA // 2) - camera_y
    ) * 0.08

    # energia
    if player["energia"] < player["max_energia"]:
        player["energia"] += 0.2

    # cooldowns
    if cooldown_espada > 0:
        cooldown_espada -= 1

    if cooldown_fruta > 0:
        cooldown_fruta -= 1

    # frutas
    verificar_frutas()

    # inimigos
    for inimigo in inimigos:

        velocidade_inimigo = inimigo["vel"]

        # gelo
        if inimigo["slow"] > 0:

            velocidade_inimigo *= 0.4

            inimigo["slow"] -= 1

        # fogo
        if inimigo["queimando"] > 0:

            inimigo["vida"] -= 0.08

            inimigo["queimando"] -= 1

            if random.randint(1, 5) == 1:

                criar_particulas(
                    inimigo["x"],
                    inimigo["y"],
                    "orange"
                )

        # luz
        if inimigo["flash"] > 0:

            velocidade_inimigo = 0

            inimigo["flash"] -= 1

        dx = player["x"] - inimigo["x"]
        dy = player["y"] - inimigo["y"]

        dist = math.hypot(dx, dy)

        if dist > 0:

            inimigo["x"] += (dx / dist) * velocidade_inimigo
            inimigo["y"] += (dy / dist) * velocidade_inimigo

        if dist < 40:
            player["vida"] -= 0.1

        if inimigo["hit"] > 0:
            inimigo["hit"] -= 1

    # respawn
    while len(inimigos) < 12:
        inimigos.append(criar_inimigo())

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

    # ilhas
    for ilha in ilhas:

        x = ilha["x"] - camera_x
        y = ilha["y"] - camera_y

        canvas.create_oval(
            x - ilha["r"],
            y - 70,

            x + ilha["r"],
            y + 70,

            fill="#8b5a2b",
            outline=""
        )

        canvas.create_rectangle(
            x - ilha["r"],
            y,

            x + ilha["r"],
            y + 50,

            fill="#3cb043",
            outline=""
        )

    # frutas
    for fruta in frutas_spawnadas[:]:

        fx = fruta["x"] - camera_x
        fy = fruta["y"] - camera_y

        cor = frutas[fruta["nome"]]["cor"]

        # brilho
        canvas.create_oval(
            fx - 22,
            fy - 22,

            fx + 22,
            fy + 22,

            fill=cor,
            outline="white",
            width=2
        )

        # fruta
        canvas.create_oval(
            fx - 15,
            fy - 15,

            fx + 15,
            fy + 15,

            fill=cor
        )

        canvas.create_text(
            fx,
            fy - 28,

            text=fruta["nome"],
            fill="white",

            font=("Arial", 9, "bold")
        )

        fruta["tempo"] -= 1

        if fruta["tempo"] <= 0:

            frutas_spawnadas.remove(fruta)

            spawnar_fruta()

    # npcs
    for npc in npcs:

        desenhar_personagem(
            npc["x"],
            npc["y"],
            "#8b5a2b",
            npc["nome"]
        )

    # inimigos
    for inimigo in inimigos:

        desenhar_personagem(
            inimigo["x"],
            inimigo["y"],
            "red",
            "Bandit",
            inimigo["hit"]
        )

    # player
    desenhar_personagem(
        player["x"],
        player["y"],
        "blue",
        f"Lv {player['level']}"
    )

    # espada
    px = player["x"] - camera_x
    py = player["y"] - camera_y

    canvas.create_line(
        px + 20,
        py,

        px + 42,
        py - 22,

        width=5,
        fill="silver"
    )

    # efeitos
    for efeito in efeitos[:]:

        if efeito["tipo"] == "slash":

            canvas.create_oval(
                px - 100,
                py - 100,

                px + 100,
                py + 100,

                outline="white",
                width=4
            )

        elif efeito["tipo"] == "fruta":

            canvas.create_oval(
                px - efeito["raio"],
                py - efeito["raio"],

                px + efeito["raio"],
                py + efeito["raio"],

                outline=efeito["cor"],
                width=6
            )

        efeito["tempo"] -= 1

        if efeito["tempo"] <= 0:
            efeitos.remove(efeito)

    # particulas
    for p in particulas[:]:

        p["x"] += p["dx"]
        p["y"] += p["dy"]

        p["vida"] -= 1

        canvas.create_oval(
            p["x"] - 2 - camera_x,
            p["y"] - 2 - camera_y,

            p["x"] + 2 - camera_x,
            p["y"] + 2 - camera_y,

            fill=p["cor"],
            outline=""
        )

        if p["vida"] <= 0:
            particulas.remove(p)

    # =====================================================
    # HUD
    # =====================================================

    # vida
    canvas.create_rectangle(
        20, 20,
        260, 45,
        fill="gray"
    )

    vida_barra = (
        player["vida"] /
        player["max_vida"]
    ) * 240

    canvas.create_rectangle(
        20, 20,
        20 + vida_barra,
        45,
        fill="red"
    )

    # energia
    canvas.create_rectangle(
        20, 55,
        260, 80,
        fill="gray"
    )

    energia_barra = (
        player["energia"] /
        player["max_energia"]
    ) * 240

    canvas.create_rectangle(
        20, 55,
        20 + energia_barra,
        80,
        fill="cyan"
    )

    # textos
    canvas.create_text(
        140, 110,
        text=f"LEVEL {player['level']}",
        font=("Arial", 13, "bold")
    )

    canvas.create_text(
        140, 140,
        text=f"$ {player['money']}",
        fill="green",
        font=("Arial", 13, "bold")
    )

    canvas.create_text(
        140, 170,
        text=f"KILLS: {player['kills']}",
        font=("Arial", 13, "bold")
    )

    # fruta atual
    canvas.create_text(
        140,
        210,

        text=f"FRUTA: {player['fruta']}",

        fill=frutas[player["fruta"]]["cor"],

        font=("Arial", 14, "bold")
    )

    # controles
    canvas.create_text(
        1080,
        40,

        text="SETAS = mover",
        font=("Arial", 11, "bold")
    )

    canvas.create_text(
        1080,
        70,

        text="SPACE = espada",
        font=("Arial", 11, "bold")
    )

    canvas.create_text(
        1080,
        100,

        text="F = fruta",
        font=("Arial", 11, "bold")
    )

    canvas.create_text(
        1080,
        130,

        text="Pegue frutas pelo mapa",
        fill="white",

        font=("Arial", 10, "bold")
    )

    # game over
    if player["vida"] <= 0:

        canvas.create_text(
            LARGURA // 2,
            ALTURA // 2,

            text="GAME OVER",
            fill="red",

            font=("Arial", 70, "bold")
        )

        return

    janela.after(16, atualizar)

# =========================================================
# START
# =========================================================

atualizar()

janela.mainloop()