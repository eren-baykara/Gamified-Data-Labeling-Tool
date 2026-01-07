import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import sqlite3
import random
from PIL import Image, ImageTk
import datetime

# --- AYARLAR ---
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data_to_label")  # Etiketlenecek resimler
OUTPUT_DIR = os.path.join(BASE_DIR, "labeled_data") # Etiketlenenler buraya
DB_FILE = "label_wars.db"

# Klasörler yoksa oluştur
for folder in [DATA_DIR, OUTPUT_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Hedef Kategoriler (Klasör İsimleri)
TARGETS = {
    "1": {"name": "Single_Color", "label": "🟦 TEK RENK (1)", "key": "1"},
    "2": {"name": "Detail", "label": "Rx DETAY (2)", "key": "2"},
    "3": {"name": "Multi_Color", "label": "🌈 ÇOK RENK (3)", "key": "3"}
}

# Çıktı klasörlerini oluştur
for key in TARGETS:
    path = os.path.join(OUTPUT_DIR, TARGETS[key]["name"])
    if not os.path.exists(path):
        os.makedirs(path)

# Motivasyon Sözleri
QUOTES = [
    "🚀 Harika gidiyorsun!", "🔥 Hızına yetişilmiyor!", 
    "👀 Gözlerinden kaçmaz!", "💎 Pixel pixel işliyorsun!",
    "🏆 Şampiyonlar ligi performansı!"
]

class LabelWarsApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Label Wars v2.0 - Oyuncu: {self.username}")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2b2b2b")
        
        self.image_list = []
        self.current_img_index = 0
        self.history = [] # Undo için
        
        self.init_db()
        self.load_images()
        self.setup_ui()
        self.show_current_image()
        self.refresh_leaderboard()

    def init_db(self):
        """Veritabanı ve tabloları oluşturur."""
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                score INTEGER DEFAULT 0,
                last_active TIMESTAMP
            )
        ''')
        # Kullanıcıyı ekle veya güncelle
        self.cursor.execute("INSERT OR IGNORE INTO users (username, score) VALUES (?, 0)", (self.username,))
        self.conn.commit()

    def update_score(self, points):
        self.cursor.execute("UPDATE users SET score = score + ? WHERE username = ?", (points, self.username))
        self.conn.commit()
        self.refresh_leaderboard()

    def load_images(self):
        """Klasördeki resimleri yükler."""
        exts = (".jpg", ".jpeg", ".png", ".webp")
        self.image_list = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(exts)]
        if not self.image_list:
            messagebox.showinfo("Bilgi", "Etiketlenecek resim kalmadı! 'data_to_label' klasörüne resim ekleyin.")

    def setup_ui(self):
        # --- Sol Panel (Resim) ---
        self.panel_left = tk.Frame(self.root, bg="#2b2b2b")
        self.panel_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lbl_img = tk.Label(self.panel_left, bg="black")
        self.lbl_img.pack(fill=tk.BOTH, expand=True)

        self.lbl_info = tk.Label(self.panel_left, text="Resim yükleniyor...", bg="#2b2b2b", fg="white", font=("Arial", 12))
        self.lbl_info.pack(pady=5)

        # --- Sağ Panel (Kontroller & Leaderboard) ---
        self.panel_right = tk.Frame(self.root, bg="#333", width=300)
        self.panel_right.pack(side=tk.RIGHT, fill=tk.Y, padx=0)
        self.panel_right.pack_propagate(False)

        # Başlık
        tk.Label(self.panel_right, text="🏆 LİDER TABLOSU", bg="#333", fg="#f1c40f", font=("Impact", 18)).pack(pady=20)
        
        self.listbox_leaderboard = tk.Listbox(self.panel_right, bg="#444", fg="white", font=("Consolas", 12), height=10, bd=0)
        self.listbox_leaderboard.pack(fill=tk.X, padx=10)

        tk.Label(self.panel_right, text="🎮 KONTROLLER", bg="#333", fg="#3498db", font=("Impact", 14)).pack(pady=20)
        
        # Butonlar
        for k, v in TARGETS.items():
            btn = tk.Button(self.panel_right, text=f"{v['label']}", bg="#555", fg="white", font=("Arial", 11, "bold"),
                            command=lambda key=k: self.move_image(key))
            btn.pack(fill=tk.X, padx=10, pady=5)
            self.root.bind(k, lambda event, key=k: self.move_image(key)) # Klavye kısayolu

        # Undo Butonu
        btn_undo = tk.Button(self.panel_right, text="↩ GERİ AL (Undo)", bg="#e74c3c", fg="white", command=self.undo_action)
        btn_undo.pack(fill=tk.X, padx=10, pady=20)

        # Motivasyon Alanı
        self.lbl_motiv = tk.Label(self.panel_right, text="", bg="#333", fg="#2ecc71", font=("Arial", 10, "italic"), wraplength=280)
        self.lbl_motiv.pack(side=tk.BOTTOM, pady=20)

    def show_current_image(self):
        if not self.image_list:
            self.lbl_img.config(image="", text="BİTTİ! 🎉")
            return

        img_name = self.image_list[0]
        img_path = os.path.join(DATA_DIR, img_name)
        
        try:
            pil_img = Image.open(img_path)
            # Resmi pencereye sığdır
            w_box, h_box = 600, 600
            pil_img.thumbnail((w_box, h_box))
            self.tk_img = ImageTk.PhotoImage(pil_img)
            self.lbl_img.config(image=self.tk_img)
            self.lbl_info.config(text=f"{img_name} ({len(self.image_list)} kaldı)")
        except Exception as e:
            print(f"Resim hatası: {e}")
            self.move_image("skip") # Hatalıysa geç

    def move_image(self, target_key):
        if not self.image_list: return

        img_name = self.image_list[0]
        src = os.path.join(DATA_DIR, img_name)
        
        if target_key == "skip":
            # Hatalıysa sadece listeden at
            self.image_list.pop(0)
            self.show_current_image()
            return

        target_folder = TARGETS[target_key]["name"]
        dst = os.path.join(OUTPUT_DIR, target_folder, img_name)

        try:
            shutil.move(src, dst)
            self.history.append({"name": img_name, "src": src, "dst": dst, "key": target_key})
            self.image_list.pop(0)
            
            # Puan ve Motivasyon
            self.update_score(1)
            self.lbl_motiv.config(text=random.choice(QUOTES))
            
            self.show_current_image()
        except Exception as e:
            messagebox.showerror("Hata", f"Taşıma hatası: {e}")

    def undo_action(self):
        if not self.history:
            messagebox.showinfo("Uyarı", "Geri alınacak işlem yok.")
            return

        last_action = self.history.pop()
        try:
            shutil.move(last_action["dst"], last_action["src"])
            self.image_list.insert(0, last_action["name"])
            self.update_score(-1) # Puanı geri al
            self.lbl_motiv.config(text="⚠️ İşlem geri alındı.")
            self.show_current_image()
        except Exception as e:
            messagebox.showerror("Hata", f"Geri alma hatası: {e}")

    def refresh_leaderboard(self):
        self.listbox_leaderboard.delete(0, tk.END)
        self.cursor.execute("SELECT username, score FROM users ORDER BY score DESC")
        for idx, (user, score) in enumerate(self.cursor.fetchall(), 1):
            prefix = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
            self.listbox_leaderboard.insert(tk.END, f"{prefix} {user}: {score}")

if __name__ == "__main__":
    # Giriş Ekranı (Basit)
    login = tk.Tk()
    login.withdraw()
    user = tk.simpledialog.askstring("Giriş", "Kullanıcı Adı:")
    if user:
        root = tk.Tk()
        app = LabelWarsApp(root, user)
        root.mainloop()
