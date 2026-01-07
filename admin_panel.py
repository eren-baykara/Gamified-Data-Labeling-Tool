import sqlite3
import os

DB_FILE = "label_wars.db"

def admin_menu():
    print("\n" + "="*40)
    print(" 👑 ETİKET SAVAŞLARI - YÖNETİCİ PANELİ")
    print("="*40)

    if not os.path.exists(DB_FILE):
        print("❌ Veritabanı bulunamadı. Önce uygulamayı çalıştırın.")
        return

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    while True:
        print("\n--- GÜNCEL PUAN DURUMU ---")
        c.execute("SELECT username, score FROM users ORDER BY score DESC")
        users = c.fetchall()
        
        if not users:
            print("⚠️ Henüz kayıtlı kullanıcı yok.")
        else:
            for u, s in users:
                print(f"👤 {u:<15} : {s} Puan")

        print("\n[1] Puan Düzenle")
        print("[2] Kullanıcı Sil")
        print("[Q] Çıkış")
        
        choice = input("Seçim: ").upper()

        if choice == 'Q':
            break
        
        elif choice == '1':
            target = input("Kullanıcı adı: ")
            try:
                new_score = int(input("Yeni Puan: "))
                c.execute("UPDATE users SET score = ? WHERE username = ?", (new_score, target))
                if c.rowcount > 0:
                    print(f"✅ {target} puanı güncellendi -> {new_score}")
                    conn.commit()
                else:
                    print("❌ Kullanıcı bulunamadı.")
            except ValueError:
                print("❌ Hatalı sayı girdiniz.")

        elif choice == '2':
            target = input("Silinecek Kullanıcı: ")
            confirm = input(f"{target} silinecek? (E/H): ")
            if confirm.upper() == 'E':
                c.execute("DELETE FROM users WHERE username = ?", (target,))
                conn.commit()
                print("✅ Kullanıcı silindi.")

    conn.close()
    print("Panel kapatıldı.")

if __name__ == "__main__":
    admin_menu()
