import tkinter as tk
import numpy as np
import sounddevice as sd
import speech_recognition as sr

# Frequências das notas musicais (em Hz)
frequencias = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63,
    "F": 349.23, "F#": 369.99, "G": 392.00, "G#": 415.30, "A": 440.00,
    "A#": 466.16, "B": 493.88
}

mapa_notas = {
    "dó": "C", "ré": "D", "mi": "E", "fá": "F", "sol": "G", "lá": "A", "si": "B",
    "dó#": "C#", "ré#": "D#", "fá#": "F#", "sol#": "G#", "l#": "A#"
}

# Função para gerar o som de uma nota
def gerar_som(frequencia, duracao=0.5, taxa_amostragem=44100):
    t = np.linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False) 
    onda = 0.5 * np.sin(2 * np.pi * frequencia * t)  
    sd.play(onda, samplerate=taxa_amostragem) 
    sd.wait()  

# Função para tocar a nota e destacar a tecla no piano
def tocar_nota(notas):
    for i, nota in enumerate(notas):
        if nota in frequencias:
            frequencia = frequencias[nota]
            janela.after(i*300, lambda f=frequencia: gerar_som(f))
            janela.after(i*300, lambda n=nota: destacar_tecla(n))
            

# Função para destacar a tecla no piano
def destacar_tecla(nota):
    print(f"Destacar Nota: {nota}")
    if nota in notas_brancas:
        index = notas_brancas.index(nota)
        canvas.itemconfig(teclas_brancas[index], fill="yellow") 
    elif nota in notas_pretas:
        index = notas_pretas.index(nota)
        canvas.itemconfig(teclas_pretas[index], fill="yellow") 


# Função para desmarcar a tecla (retornar à cor original)
def desmarcar_tecla():
    for tecla in teclas_brancas:
        canvas.itemconfig(tecla, fill="white")
    for tecla in teclas_pretas:
        canvas.itemconfig(tecla, fill="black")

# Função de reconhecimento de voz
def reconhecer_voz():
    desmarcar_tecla()
    reconhecedor = sr.Recognizer()

    with sr.Microphone() as source:
        texto_output.delete(1.0, tk.END)
        texto_output.insert(tk.END, "Diga uma nota musical...")
        janela.update()

        reconhecedor.adjust_for_ambient_noise(source) 
        audio = reconhecedor.listen(source) 

    try:
        texto = reconhecedor.recognize_google(audio, language="pt-PT")  
        texto_output.delete(1.0, tk.END) 
        texto_output.insert(tk.END, f"Nota: {texto}")

        palavras = texto.lower().split()  

        for palavra in palavras:
            if palavra in mapa_notas:  
                nota = mapa_notas[palavra]
                tocar_nota(nota)
            else:
                texto_output.insert(tk.END, f"\n'{palavra}' não é uma nota válida.")

    except sr.UnknownValueError:
        texto_output.delete(1.0, tk.END)
        texto_output.insert(tk.END, "Não entendi o que disse.")
    except sr.RequestError as e:
        texto_output.delete(1.0, tk.END)
        texto_output.insert(tk.END, f"Erro ao tentar se conectar ao serviço de reconhecimento: {e}")

# Criar a janela principal
janela = tk.Tk()
janela.title("Pitch Piano")

# Definir o tamanho da janela
janela.geometry("800x500")

# Definir a cor de fundo
janela.configure(bg="lightpink")

# Texto explicativo
texto_info = tk.Label(janela, text="Clique no botão", font=("Arial", 14), bg="lightpink")
texto_info.pack(pady=20)

# Área de texto onde o resultado será mostrado
texto_output = tk.Text(janela, height=6, width=40, wrap=tk.WORD)
texto_output.pack(pady=10)

# Botão para iniciar o reconhecimento de voz
botao_voz = tk.Button(janela, text="Falar", command=reconhecer_voz, font=("Arial", 12))
botao_voz.pack(pady=10)

# Criar um canvas para desenhar o piano
canvas = tk.Canvas(janela, width=440, height=200, bg="gray")
canvas.pack()

# Tamanho das teclas
largura_tecla = 60
altura_tecla = 200
espaco_entre_teclas = 4

# Desenhar teclas brancas
notas_brancas = ["C", "D", "E", "F", "G", "A", "B"]
teclas_brancas = []
for i, nota in enumerate(notas_brancas):
    tecla = canvas.create_rectangle(i * (largura_tecla + espaco_entre_teclas), 0,(i + 1) * largura_tecla + i * espaco_entre_teclas, altura_tecla,fill="white", outline="black")
    teclas_brancas.append(tecla)

# Desenhar teclas pretas
notas_pretas = ["C#", "D#", "F#", "G#", "A#"]
teclas_pretas = []
offset = [1, 2, 4, 5, 6]
for i, nota in enumerate(notas_pretas):
    x_offset = offset[i] * (largura_tecla + espaco_entre_teclas) - largura_tecla / 4
    tecla = canvas.create_rectangle(x_offset, 0,x_offset + largura_tecla / 2, altura_tecla - 100,fill="black", outline="black")
    teclas_pretas.append(tecla)

# Iniciar a interface gráfica
janela.mainloop()



