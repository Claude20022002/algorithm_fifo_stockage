from customtkinter import *
import matplotlib.pyplot as plt

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

        self.grid_frame = CTkFrame(self)
        self.grid_frame.pack(pady=20)

        self.status_label = CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def simulate_fifo(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        sequence = list(map(int, self.sequence_entry.get().split()))
        num_frames = int(self.frames_entry.get())

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
            CTkLabel(self.grid_frame, text=val).grid(row=max_frames + 2, column=i + 1)

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

    def show_graph(self):
        plt.figure(figsize=(10, 4))
        bars = range(len(self.page_faults))
        colors = ['red' if pf == 'X' else 'green' for pf in self.page_faults]
        plt.bar(bars, [1]*len(self.page_faults), color=colors, tick_label=list(map(str, bars)))
        plt.title("Défauts de page FIFO")
        plt.xlabel("Étapes")
        plt.ylabel("Défaut (X) ou non (✓)")
        plt.show()

if __name__ == "__main__":
    app = FIFOVisualizer()
    app.mainloop()
