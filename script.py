from customtkinter import *
import matplotlib.pyplot as plt
import tkinter.messagebox as messagebox

class FIFOVisualizer(CTk):
    def __init__(self):
        super().__init__()
        self.title("FIFO Page Replacement Visualizer")
        self.geometry("1000x600")
        self.frames = []
        self.page_faults = []
        self.current_step = 0

        # Inputs
        self.sequence_label = CTkLabel(self, text="Séquence des pages (ex: 2 3 2 1 5 2 4):")
        self.sequence_label.pack(pady=10)
        self.sequence_entry = CTkEntry(self, width=400)
        self.sequence_entry.pack()

        self.frames_label = CTkLabel(self, text="Nombre de cadres mémoire :")
        self.frames_label.pack(pady=10)
        self.frames_entry = CTkEntry(self, width=100)
        self.frames_entry.pack()

        self.simulate_btn = CTkButton(self, text="Simuler", command=self.simulate_fifo)
        self.simulate_btn.pack(pady=20)

        self.next_btn = CTkButton(self, text="Étape suivante", command=self.show_next_step, state="disabled")
        self.next_btn.pack(pady=5)

        self.reset_btn = CTkButton(self, text="Réinitialiser", command=self.reset_simulation)
        self.reset_btn.pack(pady=5)

        self.help_btn = CTkButton(self, text="Aide", command=self.show_help)
        self.help_btn.pack(pady=5)

        self.grid_frame = CTkFrame(self)
        self.grid_frame.pack(pady=20)

        self.status_label = CTkLabel(self, text="")
        self.status_label.pack(pady=10)

        self.progress_bar = CTkProgressBar(self)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

    def simulate_fifo(self):
        try:
            sequence = list(map(int, self.sequence_entry.get().split()))
            num_frames = int(self.frames_entry.get())
            if num_frames <= 0:
                raise ValueError("Le nombre de cadres doit être positif")
            if not sequence:
                raise ValueError("La séquence ne peut pas être vide")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.frames = []
        self.page_faults = []
        self.current_step = 0
        memory = []
        fifo_queue = []

        for page in sequence:
            if page not in memory:
                if len(memory) < num_frames:
                    memory.append(page)
                else:
                    memory.remove(fifo_queue.pop(0))
                    memory.append(page)
                fifo_queue.append(page)
                self.page_faults.append("X")
            else:
                self.page_faults.append("✓")
            self.frames.append(memory[:])

        self.display_grid()
        self.next_btn.configure(state="normal")
        self.status_label.configure(text=f"Nombre total de défauts de page : {self.page_faults.count('X')}")

    def display_grid(self):
        CTkLabel(self.grid_frame, text="Séquence", font=("Arial", 12, "bold")).grid(row=0, column=0)
        sequence = self.sequence_entry.get().split()
        for i, val in enumerate(sequence):
            label = CTkLabel(self.grid_frame, text=val, fg_color="gray20", corner_radius=4, width=40)
            label.grid(row=0, column=i + 1, padx=2, pady=2)

        max_frames = int(self.frames_entry.get())
        for row in range(max_frames):
            CTkLabel(self.grid_frame, text=f"Cadre {row+1}").grid(row=row + 1, column=0)
            for col in range(len(self.frames)):
                value = self.frames[col][row] if row < len(self.frames[col]) else ""
                CTkLabel(self.grid_frame, text=value, width=40, fg_color="gray10", corner_radius=4).grid(row=row + 1, column=col + 1)

        for i, val in enumerate(self.page_faults):
            color = "red" if val == "X" else "green"
            CTkLabel(self.grid_frame, text=val, fg_color=color, text_color="white").grid(row=max_frames + 2, column=i + 1)

    def show_next_step(self):
        sequence = list(map(int, self.sequence_entry.get().split()))
        if self.current_step >= len(sequence):
            self.next_btn.configure(state="disabled")
            self.show_graph()
            return

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        partial_frames = self.frames[:self.current_step + 1]
        partial_faults = self.page_faults[:self.current_step + 1]

        for i in range(self.current_step + 1):
            CTkLabel(self.grid_frame, text=sequence[i], fg_color="gray30", corner_radius=4, width=40).grid(row=0, column=i + 1)

        max_frames = int(self.frames_entry.get())
        for row in range(max_frames):
            CTkLabel(self.grid_frame, text=f"Cadre {row+1}").grid(row=row + 1, column=0)
            for col in range(self.current_step + 1):
                value = partial_frames[col][row] if row < len(partial_frames[col]) else ""
                CTkLabel(self.grid_frame, text=value, width=40, fg_color="gray10", corner_radius=4).grid(row=row + 1, column=col + 1)

        for i, val in enumerate(partial_faults):
            CTkLabel(self.grid_frame, text=val).grid(row=max_frames + 2, column=i + 1)

        self.current_step += 1
        progress = self.current_step / len(sequence)
        self.progress_bar.set(progress)

    def show_graph(self):
        plt.figure(figsize=(10, 4))
        bars = range(len(self.page_faults))
        colors = ['red' if pf == 'X' else 'green' for pf in self.page_faults]
        plt.bar(bars, [1]*len(self.page_faults), color=colors, tick_label=list(map(str, bars)))
        plt.title("Défauts de page FIFO")
        plt.xlabel("Étapes")
        plt.ylabel("Défaut (X) ou non (✓)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def reset_simulation(self):
        self.sequence_entry.delete(0, 'end')
        self.frames_entry.delete(0, 'end')
        self.current_step = 0
        self.frames = []
        self.page_faults = []
        self.next_btn.configure(state="disabled")
        self.status_label.configure(text="")
        self.progress_bar.set(0)
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

    def show_help(self):
        help_text = """
        Comment utiliser :
        1. Entrez une séquence de pages (ex: 2 3 2 1 5)
        2. Entrez le nombre de cadres mémoire
        3. Cliquez sur Simuler
        4. Utilisez 'Étape suivante' pour avancer
        5. Consultez le graphique final
        """
        messagebox.showinfo("Aide", help_text)

if __name__ == "__main__":
    app = FIFOVisualizer()
    app.mainloop()
