import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import struct
import os
import warnings

warnings.filterwarnings("ignore")

# --- FILE PATHS ---
SAVE_FILE_PATH = r"C:\Users\1\Documents\Square Enix\FINAL FANTASY X&X-2 HD Remaster\FINAL FANTASY X\ffx_000"
LEVEL_OFFSET = 0x15FA

EBP_FILE_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY FFX&FFX-2 HD Remaster\data\mods\ffx_ps2\ffx\master\jppc\event\obj\bl\bltz0000\bltz0000.ebp"

# --- CRC CONSTANTS & LOOKUP TABLE ---
CRC_START = 0x0040
CRC_SIZE = 0x64F8
CRC_BOTTOM = 0x64F4
CRC_TOP = 0x001A

CRC_MASK = [
    0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
    0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
    0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
    0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
    0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
    0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
    0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
    0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
    0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
    0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
    0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
    0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
    0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
    0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
    0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
    0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
    0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
    0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
    0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
    0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
    0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
    0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
    0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
    0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
    0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
    0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
    0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
    0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
    0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
    0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
    0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
    0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x0000
]

# The true memory offsets for each stat block inside bltz0000.ebp
STAT_OFFSETS = {
    "HP": 0x48B2D0,
    "AT": 0x48BA50,
    "EN": 0x48C1D0,
    "PA": 0x48C590,
    "SH": 0x48C950,
    "BL": 0x48CD10,
    "CA": 0x48D0D0,
    "SP": 0x48D850
}

class BlitzballApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Final Fantasy X - Blitzball Stat Architect (Full Hex Editor)")
        
        # Hardcoded Character List (Order exactly matches the game's internal memory)
        self.characters = [
            "Tidus", "Wakka", "Datto", "Letty", "Jassu", "Botta", "Keepa", "Bickson", 
            "Abus", "Graav", "Doram", "Balgerda", "Raudy", "Larbeight", "Isken", "Vuroja", 
            "Kulukan", "Deim", "Nizarut", "Eigaar", "Blappa", "Berrik", "Judda", "Lakkam", 
            "Nimrook", "Basik Ronso", "Argai Ronso", "Gazna Ronso", "Nuvy Ronso", "Irga Ronso", 
            "Zamzi Ronso", "Giera Guado", "Zazi Guado", "Navara Guado", "Auda Guado", "Pah Guado", 
            "Noy Guado", "Rin", "Tatts", "Kyou", "Shuu", "Nedus", "Biggs", "Wedge", "Ropp", 
            "Linna", "Mep", "Zalitz", "Naida", "Durren", "Jumal", "Svanda", "Vilucha", "Shaami", 
            "Zev Ronso", "Yuma Guado", "Kiyuri", "Brother", "Mifurey", "Miyu"
        ]
        
        self.char_data = {char: {} for char in self.characters}
        self.levels = {}
        
        self.stats = ["HP", "SP", "AT", "EN", "PA", "SH", "BL", "CA"]
        
        # Load data from external files
        self.read_ebp_file_stats()
        self.read_save_file_levels()
        
        # --- UI FRAMES ---
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.bottom_frame = ttk.Frame(root, padding="10")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # --- TOP CONTROLS ---
        ttk.Label(self.control_frame, text="Character:").pack(side=tk.LEFT, padx=5)
        self.char_var = tk.StringVar()
        self.char_dropdown = ttk.Combobox(self.control_frame, textvariable=self.char_var, values=self.characters, state="readonly", width=12)
        self.char_dropdown.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.control_frame, text="Stat:").pack(side=tk.LEFT, padx=5)
        self.stat_var = tk.StringVar()
        self.stat_dropdown = ttk.Combobox(self.control_frame, textvariable=self.stat_var, values=self.stats, state="readonly", width=5)
        self.stat_dropdown.pack(side=tk.LEFT, padx=5)
        
        # The Level Slider
        ttk.Label(self.control_frame, text="  Lv:").pack(side=tk.LEFT, padx=(10, 2))
        self.level_var = tk.IntVar(value=50)
        self.level_slider = ttk.Scale(self.control_frame, from_=1, to=99, variable=self.level_var, orient=tk.HORIZONTAL, length=150, command=self.on_slider_move)
        self.level_slider.pack(side=tk.LEFT, padx=5)
        
        # Randomise Button
        self.random_btn = ttk.Button(self.control_frame, text="Randomise Curve", command=self.randomise_curve)
        self.random_btn.pack(side=tk.LEFT, padx=20)
        
        # Info Label
        self.info_label = ttk.Label(self.control_frame, text="", font=("Courier", 10))
        self.info_label.pack(side=tk.LEFT, padx=10)
        
        # --- BOTTOM CONTROLS ---
        # The Save File Update Button (Level)
        self.save_lvl_btn = ttk.Button(self.bottom_frame, text="Update Save File (Level & Checksum)", command=self.save_level_to_file)
        self.save_lvl_btn.pack(side=tk.RIGHT, padx=5)
        
        # The NEW Game File Update Button (Curve Data)
        self.save_ebp_btn = ttk.Button(self.bottom_frame, text="Update Game File (Curve)", command=self.save_curve_to_ebp)
        self.save_ebp_btn.pack(side=tk.RIGHT, padx=5)
        
        # Bind events
        self.char_dropdown.bind('<<ComboboxSelected>>', self.on_selection_change)
        self.stat_dropdown.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        self.char_dropdown.set("Tidus")
        self.stat_dropdown.set("HP")
        
        # --- MATPLOTLIB SETUP ---
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Graph Elements
        self.x_fixed = np.array([0, 33, 66, 99], dtype=float)
        self.y_current = np.zeros(4)
        
        # Rendering layers
        self.dashed_box, = self.ax.plot([], [], 'b--', alpha=0.4, zorder=3)
        self.curve, = self.ax.plot([], [], 'b-', linewidth=2, zorder=4)
        self.line, = self.ax.plot([], [], 'ro', markersize=10, zorder=5)
        self.live_dot, = self.ax.plot([], [], 'bo', markersize=11, zorder=6)
        
        self.text_x_axis = self.ax.text(0, 0, "", color='blue', va='top', ha='center', fontsize=10, fontweight='bold')
        self.text_y_axis = self.ax.text(0, 0, "", color='blue', va='center', ha='right', fontsize=10, fontweight='bold')
        
        self.ax.set_xlim(-5, 105)
        self.ax.set_xticks([0, 33, 66, 99])
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        self._dragging_point = None
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.on_selection_change()

    def calculate_ffx_crc(self, file_data: bytearray) -> tuple:
        """Calculates the specific CRC matching FFX's exact logic."""
        crc_hash = 0xFFFF
        
        for i in range(CRC_START, CRC_SIZE):
            if i == CRC_BOTTOM or i == CRC_BOTTOM + 1:
                current_byte = 0
            else:
                current_byte = file_data[i]
                
            index = (current_byte ^ (crc_hash >> 8)) & 0xFF
            crc_hash = (CRC_MASK[index] ^ (crc_hash << 8)) & 0xFFFF
                    
        crc_hash ^= 0xFFFF
        return (crc_hash & 0xFF), ((crc_hash >> 8) & 0xFF)

    def read_ebp_file_stats(self):
        try:
            if os.path.exists(EBP_FILE_PATH):
                with open(EBP_FILE_PATH, "rb") as f:
                    for stat, offset in STAT_OFFSETS.items():
                        f.seek(offset)
                        for char in self.characters:
                            bytes_data = f.read(16)
                            if len(bytes_data) == 16:
                                v1, v2, v3, v4 = struct.unpack('<ffff', bytes_data)
                                self.char_data[char][stat] = (v1, v2, v3, v4)
            else:
                raise FileNotFoundError
        except Exception as e:
            messagebox.showwarning("File Error", f"Could not read EBP file at {EBP_FILE_PATH}.\nLoading dummy data.")
            for char in self.characters:
                for stat in self.stats:
                    self.char_data[char][stat] = (10.0, 0.5, 0.0, 3.0)

    def save_curve_to_ebp(self):
        char = self.char_var.get()
        stat = self.stat_var.get()
        if not char or char not in self.characters: return
        
        V1, V2, V3, V4 = self.solve_variables()
        
        try:
            char_idx = self.characters.index(char)
            base_offset = STAT_OFFSETS[stat]
            exact_offset = base_offset + (char_idx * 16)
            
            if os.path.exists(EBP_FILE_PATH):
                with open(EBP_FILE_PATH, "r+b") as f:
                    f.seek(exact_offset)
                    packed_data = struct.pack('<ffff', float(V1), float(V2), float(V3), float(V4))
                    f.write(packed_data)
                
                self.char_data[char][stat] = (V1, V2, V3, float(V4))
                messagebox.showinfo("Hex Edit Success", f"Successfully patched {char}'s {stat} curve directly into bltz0000.ebp!")
            else:
                messagebox.showerror("File Error", "EBP file not found at defined path.")
        except PermissionError:
            messagebox.showerror("Permission Denied", "Cannot write to the game file. You must run this Python script as Administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to patch game file:\n{e}")

    def read_save_file_levels(self):
        try:
            if os.path.exists(SAVE_FILE_PATH):
                with open(SAVE_FILE_PATH, "rb") as f:
                    f.seek(LEVEL_OFFSET)
                    level_bytes = f.read(60)
                    for i, char in enumerate(self.characters):
                        if i < len(level_bytes):
                            self.levels[char] = max(1, min(99, level_bytes[i]))
            else:
                raise FileNotFoundError
        except Exception:
            for char in self.characters:
                self.levels[char] = 50

    def save_level_to_file(self):
        """Modifies the level, calculates the new valid checksum, and overwrites."""
        char = self.char_var.get()
        new_lvl = self.level_var.get()
        if not char or char not in self.characters: return
        
        try:
            char_idx = self.characters.index(char)
            offset = LEVEL_OFFSET + char_idx
            if os.path.exists(SAVE_FILE_PATH):
                with open(SAVE_FILE_PATH, "r+b") as f:
                    # Read the entire file into memory
                    file_data = bytearray(f.read())
                    
                    # Apply the level edit
                    file_data[offset] = new_lvl
                    
                    # Calculate the new checksum based on the modified data
                    low_byte, high_byte = self.calculate_ffx_crc(file_data)
                    
                    # Inject the checksum into the top and bottom header locations
                    file_data[CRC_BOTTOM] = low_byte
                    file_data[CRC_BOTTOM + 1] = high_byte
                    file_data[CRC_TOP] = low_byte
                    file_data[CRC_TOP + 1] = high_byte
                    
                    # Overwrite the file on disk
                    f.seek(0)
                    f.write(file_data)
                    
                self.levels[char] = new_lvl
                messagebox.showinfo("Success", f"Successfully patched {char}'s level to {new_lvl} and secured the checksum!")
            else:
                messagebox.showerror("File Error", "Save file not found at defined path.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to patch save file:\n{e}")

    def load_equation_to_points(self, char, stat):
        v1, v2, v3, v4 = self.char_data.get(char, {}).get(stat, (0.0, 0.0, 0.0, 3.0))

        y_vals = []
        for x in self.x_fixed:
            if v4 == 1.0:
                y = v1 + (v2 * np.power(np.clip(x, 0, None), v3))
            else:
                y = v1 + (v2 * x) + (v3 * (x ** 2))
            y_vals.append(y)
            
        self.y_current = np.array(y_vals)

    @staticmethod
    def poly_func(x, v1, v2, v3): return v1 + (v2 * x) + (v3 * x**2)

    @staticmethod
    def exp_func(x, v1, v2, v3_int): return v1 + (v2 * np.power(np.clip(x, 0, None), v3_int))

    def solve_variables(self):
        v1_fixed = self.y_current[0]
        def fit_poly(x, v2, v3): return self.poly_func(x, v1_fixed, v2, v3)
        
        best_v2, best_v3, best_v4 = 0, 0, 3.0
        lowest_error = float('inf')
        
        try:
            popt_poly, _ = curve_fit(fit_poly, self.x_fixed, self.y_current, p0=[1, 0.5])
            err_poly = np.sum((self.y_current - fit_poly(self.x_fixed, *popt_poly))**2)
            if err_poly < lowest_error:
                lowest_error = err_poly
                best_v2, best_v3, best_v4 = popt_poly[0], popt_poly[1], 3.0
        except: pass

        best_exp_err, best_exp_v2, best_exp_v3 = float('inf'), 0, 1
        for test_v3 in range(1, 11):
            def fit_fixed_exp(x, v2): return self.exp_func(x, v1_fixed, v2, test_v3)
            try:
                popt_exp, _ = curve_fit(fit_fixed_exp, self.x_fixed, self.y_current, p0=[1e-5])
                err_exp = np.sum((self.y_current - fit_fixed_exp(self.x_fixed, popt_exp[0]))**2)
                if err_exp < best_exp_err:
                    best_exp_err = err_exp
                    best_exp_v2 = popt_exp[0]
                    best_exp_v3 = test_v3
            except: pass
                
        if best_exp_err < lowest_error:
            best_v2, best_v3, best_v4 = best_exp_v2, float(best_exp_v3), 1.0
            
        if best_v4 == 3.0 and abs(best_v3) < 1e-4:
            best_v3, best_v4 = 0.0, 0.0
            
        return v1_fixed, best_v2, best_v3, best_v4

    def update_graph(self):
        stat = self.stat_var.get()
        char = self.char_var.get()
        
        if stat == "HP":
            self.ax.set_ylim(0, 15000)
        else:
            self.ax.set_ylim(0, 150)
            
        V1, V2, V3, V4 = self.solve_variables()
        cx = np.linspace(0, 99, 100)
        
        if V4 == 1.0:
            cy = self.exp_func(cx, V1, V2, int(V3))
            formula_str = f"Stat = {V1:.1f} + {V2:.2e} * Lv^{int(V3)}"
        else:
            cy = self.poly_func(cx, V1, V2, V3)
            formula_str = f"Stat = {V1:.1f} + {V2:.4f}*Lv + {V3:.4f}*Lv^2"
            
        char_lvl = self.level_var.get()
        if V4 == 1.0:
            live_stat = self.exp_func(char_lvl, V1, V2, int(V3))
            stat_lv1 = self.exp_func(1, V1, V2, int(V3))
            stat_lv99 = self.exp_func(99, V1, V2, int(V3))
        else:
            live_stat = self.poly_func(char_lvl, V1, V2, V3)
            stat_lv1 = self.poly_func(1, V1, V2, V3)
            stat_lv99 = self.poly_func(99, V1, V2, V3)
        
        self.curve.set_data(cx, cy)
        self.line.set_data(self.x_fixed, self.y_current)
        
        self.live_dot.set_data([char_lvl], [live_stat])
        self.dashed_box.set_data([0, char_lvl, char_lvl], [live_stat, live_stat, 0])
        
        y_padding = 500 if stat == "HP" else 5
        self.text_x_axis.set_position((char_lvl, -y_padding))
        self.text_x_axis.set_text(f"Lv {char_lvl}")
        
        self.text_y_axis.set_position((-1, live_stat))
        self.text_y_axis.set_text(f"{live_stat:.0f}")
        
        info_txt = (f"Lv 1 Stat: {stat_lv1:.0f}  ||  Lv 99 Stat: {stat_lv99:.0f}\n"
                    f"V1:{V1:.1f} | V2:{V2:.2e} | V3:{V3:.4f} | V4:{V4:.1f}\n"
                    f"{formula_str}")
        self.info_label.config(text=info_txt)
        
        self.ax.set_title(f"{char} - {stat} Growth")
        self.canvas.draw_idle()

    def on_slider_move(self, event=None):
        self.update_graph()

    def randomise_curve(self):
        stat = self.stat_var.get()
        max_val = 15000 if stat == "HP" else 150
        random_points = np.sort(np.random.uniform(0, max_val, 4))
        self.y_current = random_points
        self.update_graph()

    def on_selection_change(self, event=None):
        char = self.char_var.get()
        stat = self.stat_var.get()
        if char and stat:
            self.level_var.set(self.levels.get(char, 50))
            self.load_equation_to_points(char, stat)
            self.update_graph()

    def on_press(self, event):
        if event.inaxes != self.ax: return
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        dx = (self.x_fixed - event.xdata) / (xlim[1] - xlim[0])
        dy = (self.y_current - event.ydata) / (ylim[1] - ylim[0])
        distances = np.sqrt(dx**2 + dy**2)
        idx = np.argmin(distances)
        if distances[idx] < 0.05:
            self._dragging_point = idx

    def on_release(self, event):
        self._dragging_point = None

    def on_motion(self, event):
        if self._dragging_point is None or event.inaxes != self.ax: return
        min_y, max_y = self.ax.get_ylim()
        self.y_current[self._dragging_point] = max(min_y, min(max_y, event.ydata))
        self.update_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlitzballApp(root)
    root.mainloop()