import tkinter as tk
from tkinter import ttk

class ScrabbleCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrabble Tile Tracker")
        self.root.configure(bg="#333333")

        # Data
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.start_count = 10
        self.tile_data = {} # Stores count and widget refs for main grid
        
        # Hand Data
        self.user_hand_letters = ["", "", "", "", "", "", ""] # Empty to start
        self.opponent_hand_letters = ["?", "?", "?", "?", "?", "?", "?"] # Hidden

        # --- LAYOUT ---
        
        # 1. Main Tile Pool Area
        self.pool_frame = tk.Frame(root, bg="#333333")
        self.pool_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.create_main_grid()

        # Separator
        ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

        # 2. Hands Area (User vs Opponent)
        self.hands_container = tk.Frame(root, bg="#2b2b2b")
        self.hands_container.pack(fill="x", padx=10, pady=(0, 20))

        # Left Side: User Hand
        self.user_frame = tk.Frame(self.hands_container, bg="#2b2b2b")
        self.user_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(self.user_frame, text="MY HAND", font=("Arial", 12, "bold"), bg="#2b2b2b", fg="white").pack(pady=5)
        self.user_tiles_frame = tk.Frame(self.user_frame, bg="#2b2b2b")
        self.user_tiles_frame.pack()
        
        # Button to set hand
        self.btn_set_hand = tk.Button(self.user_frame, text="Set My Hand", command=self.open_hand_selector, bg="#4a90e2", fg="white", relief="flat")
        self.btn_set_hand.pack(pady=10)

        # Right Side: Opponent Hand
        self.opp_frame = tk.Frame(self.hands_container, bg="#2b2b2b")
        self.opp_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        tk.Label(self.opp_frame, text="OPPONENT", font=("Arial", 12, "bold"), bg="#2b2b2b", fg="white").pack(pady=5)
        self.opp_tiles_frame = tk.Frame(self.opp_frame, bg="#2b2b2b")
        self.opp_tiles_frame.pack()
        
        # Placeholder to align with the button on the left
        tk.Label(self.opp_frame, text="", bg="#2b2b2b").pack(pady=10)

        # Initial Render of hands
        self.refresh_hands()

    def create_tile_widget(self, parent, letter, count=None, size_scale=1.0, click_callback=None):
        """
        Helper function to create a single tile. 
        If count is None, it acts like a hand tile (no number).
        If count is a number, it acts like a pool tile.
        """
        w = int(60 * size_scale)
        h = int(70 * size_scale)
        font_sz = int(20 * size_scale)
        
        # Container for the tile
        frame = tk.Frame(parent, bg="#F5DEB3", bd=3, relief="raised", width=w, height=h)
        frame.grid_propagate(False)
        frame.pack_propagate(False)

        # The Letter
        lbl_letter = tk.Label(frame, text=letter, font=("Arial", font_sz, "bold"), bg="#F5DEB3", fg="black")
        lbl_letter.pack(expand=True)

        lbl_count = None
        # The Number (only if provided)
        if count is not None:
            lbl_count = tk.Label(frame, text=str(count), font=("Arial", int(10*size_scale)), bg="#F5DEB3", fg="#555555")
            lbl_count.pack(side="bottom", pady=(0, 2))

        # Bind clicks if a callback is provided
        if click_callback:
            frame.bind("<Button-1>", lambda e: click_callback())
            lbl_letter.bind("<Button-1>", lambda e: click_callback())
            if lbl_count:
                lbl_count.bind("<Button-1>", lambda e: click_callback())

        return frame, lbl_letter, lbl_count

    def create_main_grid(self):
        max_columns = 9 # Wider grid
        
        for index, letter in enumerate(self.letters):
            row = index // max_columns
            col = index % max_columns
            
            # Create a container frame for grid placement
            grid_loc = tk.Frame(self.pool_frame, bg="#333333")
            grid_loc.grid(row=row, column=col, padx=3, pady=3)

            # Create the tile widget
            tile_frame, lbl_let, lbl_cnt = self.create_tile_widget(
                grid_loc, 
                letter, 
                count=self.start_count, 
                size_scale=0.8,
                click_callback=lambda l=letter: self.decrement_pool_tile(l)
            )
            tile_frame.pack()

            self.tile_data[letter] = {
                "count": self.start_count,
                "count_lbl": lbl_cnt,
                "frame": tile_frame,
                "letter_lbl": lbl_let
            }

    def decrement_pool_tile(self, letter):
        data = self.tile_data[letter]
        if data["count"] > 0:
            data["count"] -= 1
            data["count_lbl"].config(text=str(data["count"]))
            
            if data["count"] == 0:
                # Dim the tile
                gray = "#999999"
                data["frame"].config(bg=gray, relief="sunken")
                data["letter_lbl"].config(bg=gray, fg="#666666")
                data["count_lbl"].config(bg=gray, fg="#666666")

    # --- HAND LOGIC ---

    def refresh_hands(self):
        # Clear existing widgets
        for widget in self.user_tiles_frame.winfo_children():
            widget.destroy()
        for widget in self.opp_tiles_frame.winfo_children():
            widget.destroy()

        # Draw User Hand
        for letter in self.user_hand_letters:
            display_char = letter if letter else " "
            # Use separate container to pack horizontally
            container = tk.Frame(self.user_tiles_frame, bg="#2b2b2b")
            container.pack(side="left", padx=2)
            t_frame, _, _ = self.create_tile_widget(container, display_char, size_scale=0.7)
            t_frame.pack()

        # Draw Opponent Hand
        for letter in self.opponent_hand_letters:
            container = tk.Frame(self.opp_tiles_frame, bg="#2b2b2b")
            container.pack(side="left", padx=2)
            t_frame, _, _ = self.create_tile_widget(container, letter, size_scale=0.7)
            t_frame.pack()

    def open_hand_selector(self):
        # Create a popup window (Toplevel)
        popup = tk.Toplevel(self.root)
        popup.title("Select Your Tiles")
        popup.geometry("400x150")
        popup.configure(bg="#f0f0f0")

        tk.Label(popup, text="Select the 7 tiles in your hand:", bg="#f0f0f0").pack(pady=10)

        # Container for dropdowns
        combo_frame = tk.Frame(popup, bg="#f0f0f0")
        combo_frame.pack()

        # List of options (A-Z + Blank)
        options = [""] + list(self.letters) 
        
        self.comboboxes = []

        # Create 7 dropdowns
        for i in range(7):
            cb = ttk.Combobox(combo_frame, values=options, width=3, state="readonly")
            cb.pack(side="left", padx=5)
            # Pre-select current value if exists
            current_val = self.user_hand_letters[i]
            if current_val in options:
                cb.set(current_val)
            self.comboboxes.append(cb)

        # Save Button
        btn_save = tk.Button(popup, text="Update Hand", command=lambda: self.save_hand(popup), bg="#4CAF50", fg="white")
        btn_save.pack(pady=20)

    def save_hand(self, popup_window):
        # Read values from dropdowns
        new_hand = []
        for cb in self.comboboxes:
            val = cb.get()
            new_hand.append(val)
        
        self.user_hand_letters = new_hand
        self.refresh_hands()
        popup_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x650")
    app = ScrabbleCounter(root)
    root.mainloop()