import customtkinter as ctk
import tkinter.messagebox
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def fifo_simulation(pages, nb_frames):
    memory = []
    queue = []
    steps = []
    page_faults = 0

    for page in pages:
        fault = False
        if page not in memory:
            fault = True
            page_faults += 1
            if len(memory) < nb_frames:
                memory.append(page)
                queue.append(page)
            else:
                oldest = queue.pop(0)
                memory.remove(oldest)
                memory.append(page)
                queue.append(page)
        steps.append((page, memory.copy(), fault))
    return steps, page_faults

class FifoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Animation FIFO - Gestion Mémoire")
        self.geometry("900x700")
        
        self.current_step = 0
        self.steps = []
        self.nb_frames = 0

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Frame pour les contrôles
        self.control_frame = ctk.CTkFrame(self.frame)
        self.control_frame.pack(pady=10, fill="x")

        self.label_pages = ctk.CTkLabel(self.control_frame, text="Séquence de pages (ex: 7,0,1,2,0,3,0,4):")
        self.label_pages.pack(pady=5)

        self.entry_pages = ctk.CTkEntry(self.control_frame, width=400)
        self.entry_pages.pack(pady=5)

        self.label_frames = ctk.CTkLabel(self.control_frame, text="Nombre de cadres mémoire :")
        self.label_frames.pack(pady=5)

        self.entry_frames = ctk.CTkEntry(self.control_frame, width=100)
        self.entry_frames.pack(pady=5)

        # Frame pour les boutons
        self.button_frame = ctk.CTkFrame(self.control_frame)
        self.button_frame.pack(pady=10)

        self.button_run = ctk.CTkButton(self.button_frame, text="Démarrer la simulation", command=self.run_simulation)
        self.button_run.pack(side="left", padx=5)

        self.button_step = ctk.CTkButton(self.button_frame, text="Étape suivante", command=self.next_step, state="disabled")
        self.button_step.pack(side="left", padx=5)

        self.button_graph = ctk.CTkButton(self.button_frame, text="Afficher graphique", command=self.show_graph, state="disabled")
        self.button_graph.pack(side="left", padx=5)

        self.canvas = ctk.CTkFrame(self.frame, fg_color="white", height=200)
        self.canvas.pack(pady=10, fill="x")

        self.status_label = ctk.CTkLabel(self.frame, text="")
        self.status_label.pack(pady=5)

    def run_simulation(self):
        try:
            pages = list(map(int, self.entry_pages.get().split(",")))
            self.nb_frames = int(self.entry_frames.get())
            if self.nb_frames <= 0:
                raise ValueError

            self.steps, faults = fifo_simulation(pages, self.nb_frames)
            self.current_step = 0
            self.status_label.configure(text=f"Défauts de page : {faults}")
            
            # Activer les boutons
            self.button_step.configure(state="normal")
            self.button_graph.configure(state="normal")
            
            # Afficher la première étape
            self.display_step()

        except ValueError:
            tkinter.messagebox.showerror("Erreur", "Entrée invalide. Vérifie la séquence et le nombre de cadres.")

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.display_step()
        else:
            self.button_step.configure(state="disabled")

    def display_step(self):
        # Nettoyer l'ancien affichage
        for widget in self.canvas.winfo_children():
            widget.destroy()

        box_width = 80
        padding = 20

        boxes = [ctk.CTkLabel(self.canvas, text=" ", width=box_width, height=60,
                               corner_radius=10, fg_color="#e0e0e0", text_color="black")
                 for _ in range(self.nb_frames)]

        for i, box in enumerate(boxes):
            box.place(x=i * (box_width + padding) + 100, y=50)

        page, memory, fault = self.steps[self.current_step]
        for i in range(self.nb_frames):
            if i < len(memory):
                boxes[i].configure(text=str(memory[i]),
                                   fg_color="#f87171" if fault and memory[i] == page else "#86efac")
            else:
                boxes[i].configure(text=" ", fg_color="#e0e0e0")

    def show_graph(self):
        # Créer une nouvelle fenêtre pour le graphique
        graph_window = ctk.CTkToplevel(self)
        graph_window.title("Graphique des défauts de page")
        graph_window.geometry("600x400")

        # Créer la figure matplotlib
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Calculer les défauts cumulatifs
        cumulative_faults = []
        current_faults = 0
        for step in self.steps:
            if step[2]:  # Si c'est un défaut de page
                current_faults += 1
            cumulative_faults.append(current_faults)

        # Tracer le graphique
        ax.plot(range(1, len(self.steps) + 1), cumulative_faults, 'b-', marker='o')
        ax.set_xlabel('Étapes')
        ax.set_ylabel('Défauts de page cumulés')
        ax.set_title('Évolution des défauts de page')
        ax.grid(True)

        # Intégrer le graphique dans la fenêtre Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = FifoApp()
    app.mainloop()
