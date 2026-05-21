# =========================================================
# MINI BLOX FRUITS - ULTRA EDITION
# Melhorado:
# - animações
# - combo
# - dash visual
# - IA melhor
# - boss skill
# - partículas
# - barra de boss
# - regeneração
# - hit flash
# - câmera suave
# - aura
# - mini mapa melhor
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
janela.title("Mini Blox Fruits Ultra Edition")

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

camera_suave_x = 0
camera_suave_y = 0

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

    "fruta": "fogo",

    "espada": "Katana",

    "combo": 0,

    "invencivel": 0,

    "transformado": False,

    "hit_flash": 0
}

# =========================================================
# ESPADAS
# =========================================================

espadas = {
    "Katana": 20,
    "Saber": 35,
    "Dark Blade": 60
}

# =========================================================
# COOLDOWNS
# =========================================================

cooldown_espada = 0
cooldown_dash = 0
cooldown_fruta = 0

# =========================================================
# TECLAS
# =========================================================

teclas = set()

def tecla_press(event):

    teclas.add(event.keysym)

    if event.keysym == "space":
        atacar()

    if event.keysym.lower() == "f":
        usar_fruta()

    if event.keysym.lower() == "q":
        transformar()

def tecla_release(event):

    if event.keysym in teclas:
        teclas.remove(event.keysym)

janela.bind("<KeyPress>", tecla_press)
janela.bind("<KeyRelease>", tecla_release)

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
        "fala": "Use F para poder!"
    },

    {
        "x": 3000,
        "y": 1200,
        "nome": "Sword Dealer",
        "fala": "Dark Blade = $500"
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

        "hit": 0
    }

def criar_boss():

    return {
        "x": 3500,
        "y": 1600,

        "vida": 800,
        "max_vida": 800,

        "vel": 1.2,

        "boss": True,

        "cooldown": 0,

        "hit": 0
    }

for _ in range(12):
    inimigos.append(criar_inimigo())

boss_spawnado = False

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

        player["max_energia"] += 10

        player["dano"] += 5

# =========================================================
# TRANSFORMAR
# =========================================================

def transformar():

    if player["energia"] < 50:
        return

    player["transformado"] = not player["transformado"]

# =========================================================
# PARTÍCULAS
# =========================================================

def criar_particulas(x, y, cor):

    for _ in range(12):

        particulas.append({
            "x": x,
            "y": y,

            "dx": random.uniform(-4, 4),
            "dy": random.uniform(-4, 4),

            "vida": random.randint(15, 30),

            "cor": cor
        })

# =========================================================
# ATAQUE
# =========================================================

def atacar():

    global cooldown_espada

    if cooldown_espada > 0:
        return

    cooldown_espada = 12

    player["combo"] += 1

    if player["combo"] > 3:
        player["combo"] = 1

    raio = 90 + player["combo"] * 10

    dano = player["dano"]

    if player["transformado"]:
        dano *= 2

    efeitos.append({
        "tipo": "slash",
        "tempo": 8,
        "raio": raio
    })

    for inimigo in inimigos[:]:

        dx = inimigo["x"] - player["x"]
        dy = inimigo["y"] - player["y"]

        dist = math.hypot(dx, dy)

        if dist < raio:

            inimigo["vida"] -= dano

            inimigo["hit"] = 5

            criar_particulas(
                inimigo["x"],
                inimigo["y"],
                "red"
            )

            # knockback
            if dist != 0:

                inimigo["x"] += (dx / dist) * 50
                inimigo["y"] += (dy / dist) * 50

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# FRUTA
# =========================================================

def usar_fruta():

    global cooldown_fruta

    if cooldown_fruta > 0:
        return

    if player["energia"] < 35:
        return

    player["energia"] -= 35

    cooldown_fruta = 45

    efeitos.append({
        "tipo": "fruta",
        "tempo": 18
    })

    for inimigo in inimigos[:]:

        dist = math.hypot(
            inimigo["x"] - player["x"],
            inimigo["y"] - player["y"]
        )

        if dist < 240:

            dano = player["dano"] * 2.5

            inimigo["vida"] -= dano

            inimigo["hit"] = 8

            criar_particulas(
                inimigo["x"],
                inimigo["y"],
                "orange"
            )

            if inimigo["vida"] <= 0:
                matar_inimigo(inimigo)

# =========================================================
# MATAR
# =========================================================

def matar_inimigo(inimigo):

    if inimigo in inimigos:
        inimigos.remove(inimigo)

    if inimigo["boss"]:

        ganhar_xp(300)

        player["money"] += 1000

    else:

        ganhar_xp(25)

        player["money"] += random.randint(15, 40)

    player["kills"] += 1

# =========================================================
# PERSONAGEM
# =========================================================

def desenhar_personagem(x, y, cor, nome=None, hit=0):

    x -= camera_suave_x
    y -= camera_suave_y

    # aura
    if cor == "blue" and player["transformado"]:

        canvas.create_oval(
            x - 38,
            y - 58,

            x + 38,
            y + 48,

            outline="yellow",
            width=4
        )

    # hit flash
    if hit > 0:
        cor = "white"

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

        fill=cor,
        outline="black"
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

    # olhos
    canvas.create_oval(
        x - 5,
        y - 20,

        x - 2,
        y - 17,

        fill="black"
    )

    canvas.create_oval(
        x + 2,
        y - 20,

        x + 5,
        y - 17,

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

    global camera_suave_x
    global camera_suave_y

    global cooldown_espada
    global cooldown_dash
    global cooldown_fruta

    global boss_spawnado

    # =====================================================
    # MOVIMENTO
    # =====================================================

    velocidade = player["vel"]

    if player["y"] > 1500:
        velocidade = 2

    if "Shift_L" in teclas and cooldown_dash <= 0:

        cooldown_dash = 50

        criar_particulas(
            player["x"],
            player["y"],
            "white"
        )

        if "Left" in teclas:
            player["x"] -= 180

        if "Right" in teclas:
            player["x"] += 180

        if "Up" in teclas:
            player["y"] -= 180

        if "Down" in teclas:
            player["y"] += 180

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

    # =====================================================
    # CAMERA SUAVE
    # =====================================================

    alvo_x = player["x"] - LARGURA // 2
    alvo_y = player["y"] - ALTURA // 2

    camera_suave_x += (alvo_x - camera_suave_x) * 0.08
    camera_suave_y += (alvo_y - camera_suave_y) * 0.08

    # =====================================================
    # REGEN
    # =====================================================

    if player["energia"] < player["max_energia"]:
        player["energia"] += 0.2

    if player["vida"] < player["max_vida"]:
        player["vida"] += 0.03

    # =====================================================
    # COOLDOWNS
    # =====================================================

    if cooldown_espada > 0:
        cooldown_espada -= 1

    if cooldown_dash > 0:
        cooldown_dash -= 1

    if cooldown_fruta > 0:
        cooldown_fruta -= 1

    # =====================================================
    # ENEMIES
    # =====================================================

    for inimigo in inimigos:

        dx = player["x"] - inimigo["x"]
        dy = player["y"] - inimigo["y"]

        dist = math.hypot(dx, dy)

        if dist > 0:

            inimigo["x"] += (dx / dist) * inimigo["vel"]
            inimigo["y"] += (dy / dist) * inimigo["vel"]

        # boss skill
        if inimigo["boss"]:

            inimigo["cooldown"] += 1

            if inimigo["cooldown"] > 180:

                inimigo["cooldown"] = 0

                criar_particulas(
                    player["x"],
                    player["y"],
                    "purple"
                )

                player["vida"] -= 10

        if dist < 40:

            if inimigo["boss"]:
                player["vida"] -= 0.5
            else:
                player["vida"] -= 0.15

            player["hit_flash"] = 3

        if inimigo["hit"] > 0:
            inimigo["hit"] -= 1

    # =====================================================
    # RESPAWN
    # =====================================================

    while len([i for i in inimigos if not i["boss"]]) < 12:
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
        -camera_suave_x,
        1500 - camera_suave_y,

        MAPA_LARGURA - camera_suave_x,
        MAPA_ALTURA - camera_suave_y,

        fill="#1f75fe",
        outline=""
    )

    # ilhas
    for ilha in ilhas:

        x = ilha["x"] - camera_suave_x
        y = ilha["y"] - camera_suave_y

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

    # npcs
    for npc in npcs:

        desenhar_personagem(
            npc["x"],
            npc["y"],
            "#6b3f1f",
            npc["nome"]
        )

    # inimigos
    for inimigo in inimigos:

        cor = "purple" if inimigo["boss"] else "red"

        nome = "BOSS" if inimigo["boss"] else "Bandit"

        desenhar_personagem(
            inimigo["x"],
            inimigo["y"],
            cor,
            nome,
            inimigo["hit"]
        )

    # player
    desenhar_personagem(
        player["x"],
        player["y"],
        "blue",
        f"Lv {player['level']}",
        player["hit_flash"]
    )

    # espada
    px = player["x"] - camera_suave_x
    py = player["y"] - camera_suave_y

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
                px - efeito["raio"],
                py - efeito["raio"],

                px + efeito["raio"],
                py + efeito["raio"],

                outline="white",
                width=4
            )

        elif efeito["tipo"] == "fruta":

            canvas.create_oval(
                px - 240,
                py - 240,

                px + 240,
                py + 240,

                outline="orange",
                width=6
            )

        efeito["tempo"] -= 1

        if efeito["tempo"] <= 0:
            efeitos.remove(efeito)

    # partículas
    for p in particulas[:]:

        p["x"] += p["dx"]
        p["y"] += p["dy"]

        p["vida"] -= 1

        canvas.create_oval(
            p["x"] - 2 - camera_suave_x,
            p["y"] - 2 - camera_suave_y,

            p["x"] + 2 - camera_suave_x,
            p["y"] + 2 - camera_suave_y,

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

    canvas.create_text(
        140,
        32,

        text=f"HP {int(player['vida'])}/{player['max_vida']}",
        fill="white",

        font=("Arial", 11, "bold")
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

    # xp
    xp_max = player["level"] * 60

    canvas.create_rectangle(
        20, 90,
        260, 105,
        fill="gray"
    )

    xp_barra = (
        player["xp"] /
        xp_max
    ) * 240

    canvas.create_rectangle(
        20, 90,
        20 + xp_barra,
        105,
        fill="yellow"
    )

    # textos
    canvas.create_text(
        140, 130,
        text=f"LEVEL {player['level']}",
        font=("Arial", 14, "bold")
    )

    canvas.create_text(
        140, 160,
        text=f"$ {player['money']}",
        fill="green",
        font=("Arial", 14, "bold")
    )

    canvas.create_text(
        140, 190,
        text=f"KILLS: {player['kills']}",
        font=("Arial", 12, "bold")
    )

    canvas.create_text(
        140, 220,
        text=f"FRUTA: {player['fruta']}",
        font=("Arial", 12, "bold")
    )

    # barra boss
    for inimigo in inimigos:

        if inimigo["boss"]:

            canvas.create_rectangle(
                340, 20,
                940, 45,
                fill="gray"
            )

            boss_hp = (
                inimigo["vida"] /
                inimigo["max_vida"]
            ) * 600

            canvas.create_rectangle(
                340, 20,
                340 + boss_hp,
                45,
                fill="purple"
            )

            canvas.create_text(
                640,
                32,

                text="BOSS",
                fill="white",

                font=("Arial", 12, "bold")
            )

    # mini mapa
    canvas.create_rectangle(
        1050, 500,
        1250, 700,

        fill="black"
    )

    mini_x = 1050 + (player["x"] / MAPA_LARGURA) * 200
    mini_y = 500 + (player["y"] / MAPA_ALTURA) * 200

    canvas.create_oval(
        mini_x - 4,
        mini_y - 4,

        mini_x + 4,
        mini_y + 4,

        fill="white"
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

    if player["hit_flash"] > 0:
        player["hit_flash"] -= 1

    janela.after(16, atualizar)

# =========================================================
# START
# =========================================================

atualizar()

janela.mainloop()