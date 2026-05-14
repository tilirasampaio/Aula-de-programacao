import tkinter as tk
import random
import math

# ==========================================
# CONFIGURAÇÕES
# ==========================================

LARGURA = 1000
ALTURA = 700

janela = tk.Tk()
janela.title("Mini Blox Fruits Deluxe")

canvas = tk.Canvas(
    janela,
    width=LARGURA,
    height=ALTURA,
    bg="#6ec6ff"
)
canvas.pack()

# ==========================================
# PLAYER
# ==========================================

player = {
    "x": 500,
    "y": 350,
    "vida": 100,
    "max_vida": 100,
    "level": 1,
    "xp": 0,
    "dano": 20,
    "energia": 100
}

# ==========================================
# INIMIGOS
# ==========================================

inimigos = []

def criar_inimigo():
    return {
        "x": random.randint(50, 950),
        "y": random.randint(50, 650),
        "vida": 50,
        "max_vida": 50,
        "vel": random.uniform(1, 2)
    }

for _ in range(8):
    inimigos.append(criar_inimigo())

# ==========================================
# CONTROLES
# ==========================================

teclas = set()

def tecla_press(event):
    teclas.add(event.keysym)

    # Espada
    if event.keysym == "space":
        atacar_espada()

    # Fruta
    if event.keysym.lower() == "f":
        poder_fruta()

def tecla_release(event):
    teclas.discard(event.keysym)

janela.bind("<KeyPress>", tecla_press)
janela.bind("<KeyRelease>", tecla_release)

# ==========================================
# SISTEMA XP
# ==========================================

def ganhar_xp(valor):
    player["xp"] += valor

    xp_necessario = player["level"] * 50

    if player["xp"] >= xp_necessario:
        player["xp"] = 0
        player["level"] += 1
        player["max_vida"] += 20
        player["vida"] = player["max_vida"]
        player["dano"] += 5

# ==========================================
# ATAQUE ESPADA
# ==========================================

efeitos = []

def atacar_espada():

    efeitos.append({
        "tipo": "espada",
        "tempo": 10
    })

    for inimigo in inimigos[:]:

        dist = math.hypot(
            inimigo["x"] - player["x"],
            inimigo["y"] - player["y"]
        )

        if dist < 70:

            inimigo["vida"] -= player["dano"]

            if inimigo["vida"] <= 0:
                inimigos.remove(inimigo)
                ganhar_xp(25)

# ==========================================
# PODER FRUTA
# ==========================================

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

        if dist < 150:

            inimigo["vida"] -= player["dano"] * 2

            if inimigo["vida"] <= 0:
                inimigos.remove(inimigo)
                ganhar_xp(40)

# ==========================================
# LOOP PRINCIPAL
# ==========================================

def atualizar():

    # ======================================
    # MOVIMENTO PLAYER
    # ======================================

    velocidade = 5

    if "Left" in teclas:
        player["x"] -= velocidade

    if "Right" in teclas:
        player["x"] += velocidade

    if "Up" in teclas:
        player["y"] -= velocidade

    if "Down" in teclas:
        player["y"] += velocidade

    # Limites
    player["x"] = max(20, min(LARGURA - 20, player["x"]))
    player["y"] = max(20, min(ALTURA - 20, player["y"]))

    # ======================================
    # RECUPERAR ENERGIA
    # ======================================

    if player["energia"] < 100:
        player["energia"] += 0.2

    # ======================================
    # IA INIMIGOS
    # ======================================

    for inimigo in inimigos:

        dx = player["x"] - inimigo["x"]
        dy = player["y"] - inimigo["y"]

        dist = math.hypot(dx, dy)

        if dist > 0:

            inimigo["x"] += (dx / dist) * inimigo["vel"]
            inimigo["y"] += (dy / dist) * inimigo["vel"]

        # Dano no player
        if dist < 25:
            player["vida"] -= 0.1

    # ======================================
    # RESPAWN INIMIGOS
    # ======================================

    while len(inimigos) < 8:
        inimigos.append(criar_inimigo())

    # ======================================
    # DESENHO
    # ======================================

    canvas.delete("all")

    # Céu
    canvas.create_rectangle(
        0, 0,
        LARGURA, ALTURA,
        fill="#6ec6ff",
        outline=""
    )

    # Chão
    canvas.create_rectangle(
        0, 550,
        LARGURA, ALTURA,
        fill="#3cb043",
        outline=""
    )

    # Sol
    canvas.create_oval(
        820, 40,
        920, 140,
        fill="yellow",
        outline=""
    )

    # ======================================
    # PLAYER
    # ======================================

    canvas.create_rectangle(
        player["x"] - 20,
        player["y"] - 20,
        player["x"] + 20,
        player["y"] + 20,
        fill="blue"
    )

    # Nome
    canvas.create_text(
        player["x"],
        player["y"] - 30,
        text=f"Lv {player['level']}",
        fill="white",
        font=("Arial", 10, "bold")
    )

    # ======================================
    # EFEITOS
    # ======================================

    for efeito in efeitos[:]:

        if efeito["tipo"] == "espada":

            canvas.create_oval(
                player["x"] - 70,
                player["y"] - 70,
                player["x"] + 70,
                player["y"] + 70,
                outline="white",
                width=3
            )

        elif efeito["tipo"] == "fruta":

            canvas.create_oval(
                player["x"] - 150,
                player["y"] - 150,
                player["x"] + 150,
                player["y"] + 150,
                outline="orange",
                width=5
            )

        efeito["tempo"] -= 1

        if efeito["tempo"] <= 0:
            efeitos.remove(efeito)

    # ======================================
    # INIMIGOS
    # ======================================

    for inimigo in inimigos:

        canvas.create_rectangle(
            inimigo["x"] - 18,
            inimigo["y"] - 18,
            inimigo["x"] + 18,
            inimigo["y"] + 18,
            fill="red"
        )

        # Vida inimigo
        canvas.create_rectangle(
            inimigo["x"] - 20,
            inimigo["y"] - 30,
            inimigo["x"] + 20,
            inimigo["y"] - 24,
            fill="gray"
        )

        vida_largura = (
            inimigo["vida"] /
            inimigo["max_vida"]
        ) * 40

        canvas.create_rectangle(
            inimigo["x"] - 20,
            inimigo["y"] - 30,
            inimigo["x"] - 20 + vida_largura,
            inimigo["y"] - 24,
            fill="lime"
        )

    # ======================================
    # HUD
    # ======================================

    # Vida
    canvas.create_text(
        100,
        20,
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
        20 + vida_barra, 50,
        fill="red"
    )

    # Energia
    canvas.create_text(
        100,
        70,
        text="ENERGIA",
        font=("Arial", 12, "bold")
    )

    canvas.create_rectangle(
        20, 80,
        220, 100,
        fill="gray"
    )

    canvas.create_rectangle(
        20, 80,
        20 + player["energia"] * 2, 100,
        fill="cyan"
    )

    # XP
    canvas.create_text(
        100,
        120,
        text=f"LEVEL {player['level']} | XP {player['xp']}",
        font=("Arial", 12, "bold")
    )

    # Controles
    canvas.create_text(
        780,
        30,
        text="SETAS = mover",
        font=("Arial", 12, "bold")
    )

    canvas.create_text(
        780,
        60,
        text="ESPAÇO = espada",
        font=("Arial", 12, "bold")
    )

    canvas.create_text(
        780,
        90,
        text="F = fruta",
        font=("Arial", 12, "bold")
    )

    # ======================================
    # GAME OVER
    # ======================================

    if player["vida"] <= 0:

        canvas.create_text(
            LARGURA // 2,
            ALTURA // 2,
            text="GAME OVER",
            fill="red",
            font=("Arial", 50, "bold")
        )

        return

    janela.after(16, atualizar)

# ==========================================
# INICIAR
# ==========================================

atualizar()

janela.mainloop()