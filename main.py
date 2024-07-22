#############
#iseeu && Amarok - pr3c programming team#
#############

import threading
import os
import random
import webbrowser

try:
    import httpx
    import customtkinter as ctk
    import win32gui
    import win32.lib.win32con as win32con
except ModuleNotFoundError:
    os.system("pip install httpx")
    os.system("pip install customtkinter")
    os.system("pip install win32gui")
    os.system("pip install pypiwin32")

dark_purple = "#4B0082"
light_purple = "#9370DB"

with open("data/tokens.txt", "r+") as f:
    token_list = f.read().splitlines()

with open("data/proxies.txt", "r+") as f:
    proxies_list = f.read().splitlines()

win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)

#---------------------------------------------------------------------------------------#

class AnaPencere:
    def __init__(self):
        self.main = ctk.CTk()
        self.main.geometry("1000x600")
        self.main.minsize(1000, 600)
        self.main.maxsize(1000, 600)
        self.main.title(f"GUI Token Checker by pr3c.fun - github.com/iseeuXD")
        self.bilgi_frame = ctk.CTkFrame(master=self.main, border_color="black", width=980, height=100)
        self.bilgi_frame.grid(row=0, column=0, padx=10, pady=(10, 5))
        self.button = ctk.CTkButton(master=self.bilgi_frame, text="GitHub", fg_color=dark_purple, hover_color=light_purple, font=("Roboto", 20, "bold"), width=313, command=self.github_ac)
        self.button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="we")
        self.button = ctk.CTkButton(master=self.bilgi_frame, text="Discord", fg_color=dark_purple, hover_color=light_purple, font=("Roboto", 20, "bold"), width=314, command=self.discord_ac)
        self.button.grid(row=0, column=1, padx=5, pady=10, sticky="we")
        self.button = ctk.CTkButton(master=self.bilgi_frame, text="prec.fun", fg_color=dark_purple, hover_color=light_purple, font=("Roboto", 20, "bold"), width=313, command=self.website_ac)
        self.button.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="we")
        self.kontrol_frame = ctk.CTkFrame(master=self.main, width=980, height=460)
        self.kontrol_frame.grid(row=1, column=0, padx=10, pady=5)
        self.yuklenen = ctk.CTkFrame(master=self.kontrol_frame, width=980, height=200)
        self.yuklenen.grid(row=0, column=0, padx=10, pady=10)
        self.text = ctk.CTkLabel(master=self.yuklenen, text=f"Tokenlar: {len(token_list)}", fg_color="transparent", font=("Roboto", 20, "bold"))
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.text = ctk.CTkLabel(master=self.yuklenen, text=f"Proxyler: {len(proxies_list)}", fg_color="transparent", font=("Roboto", 20, "bold"))
        self.text.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.proxy_acik_kapat = ctk.StringVar(value="kapalı")
        self.switch = ctk.CTkSwitch(master=self.kontrol_frame, text="Proxy Kullan", progress_color=dark_purple, font=("Roboto", 20, "bold"), variable=self.proxy_acik_kapat, onvalue="açık", offvalue="kapalı")
        self.switch.grid(row=1, column=0, padx=(415, 10), pady=10, sticky="nswe")
        self.button_kontrol = ctk.CTkButton(master=self.kontrol_frame, text="Kontrol Et", fg_color=dark_purple, hover_color=light_purple, font=("Roboto", 20, "bold"), width=450, command=self.kontrol)
        self.button_kontrol.grid(row=2, column=0, padx=10, pady=5, sticky="we")
        self.progressbar = ctk.CTkProgressBar(master=self.kontrol_frame, orientation="horizontal", progress_color=dark_purple, mode="indeterminate", width=960)
        self.progressbar.grid(row=3, column=0, padx=10, pady=(15, 10), sticky="nswe")
        self.progressbar.set(0)
        self.kontrol_textbox = ctk.CTkTextbox(master=self.main, font=("Roboto", 18), width=980, height=325)
        self.kontrol_textbox.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="we")
        self.kontrol_textbox.configure(state="disabled")
        self.main.mainloop()
    
    def kontrol(self):
        self.secenek = self.proxy_acik_kapat.get()
        if self.secenek == "kapalı":
            threading.Thread(target=self.proxy_kullanilmadan_kontrol).start()
        elif self.secenek == "açık":
            threading.Thread(target=self.proxy_ile_kontrol).start()

    def proxy_kullanilmadan_kontrol(self):
        self.button_kontrol.configure(state="disabled")
        self.kontrol_textbox.configure(state="normal")
        self.kontrol_textbox.insert("0.0", f"\n\n\n")
        self.progressbar.set(0)
        self.progressbar.start()
        open('result/valid.txt', 'w').close()
        open('result/invalid.txt', 'w').close()
        open('result/locked.txt', 'w').close()
        gecerli = 0
        gecersiz = 0
        kilitli = 0
        for token in token_list:
            r = httpx.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
            if r.status_code == 200:
                console_token = token.split('.')
                self.kontrol_textbox.insert("0.0", f"GEÇERLİ    -     {console_token[0]}.{console_token[1]}.********************************************\n")
                with open("result/valid.txt","a") as f:
                    f.write(f"{token}\n")
                gecerli += 1
            elif r.status_code == 401:
                self.kontrol_textbox.insert("0.0", f"GEÇERSİZ -     {token}\n")
                with open("result/invalid.txt","a") as f:
                    f.write(f"{token}\n")
                gecersiz += 1
            elif r.status_code == 403:
                self.kontrol_textbox.insert("0.0", f"KİLİTLİ      -     {token}\n")
                with open("result/locked.txt","a") as f:
                    f.write(f"{token}\n")
                kilitli += 1
        self.kontrol_textbox.insert("0.0", f"tokens.txt dosyasını başarıyla kontrol ettim (Proxy kullanılmadan)      -      Sonuç: [{gecerli} Geçerli] [{gecersiz} Geçersiz] [{kilitli} Telefon Kilitli]      -      Kayıt edildi: /result\n\n")
        self.kontrol_textbox.configure(state="disabled")
        self.progressbar.stop()
        self.button_kontrol.configure(state="normal")

    def proxy_ile_kontrol(self):
        self.button_kontrol.configure(state="disabled")
        self.kontrol_textbox.configure(state="normal")
        self.kontrol_textbox.insert("0.0", f"\n\n\n")
        self.progressbar.set(0)
        self.progressbar.start()
        open('result/valid.txt', 'w').close()
        open('result/invalid.txt', 'w').close()
        open('result/locked.txt', 'w').close()
        self.gecerli = 0
        self.gecersiz = 0
        self.kilitli = 0
        self.thread_sayisi = 0
        self.sayi = 0
        while True:
            if self.thread_sayisi <= 10:
                for token in token_list:  
                    random_proxy = "http://" + random.choice(proxies_list).strip()
                    threading.Thread(target=self.proxy_ile_token_kontrol, args=(token, random_proxy)).start()

            if self.sayi == len(token_list):
                break
        self.kontrol_textbox.insert("0.0", f"tokens.txt dosyasını başarıyla kontrol ettim (Proxy ile)      -      Sonuç: [{self.gecerli} Geçerli] [{self.gecersiz} Geçersiz] [{self.kilitli} Telefon Kilitli]      -      Kayıt edildi: /result\n\n")
        self.kontrol_textbox.configure(state="disabled")
        self.progressbar.stop()
        self.button_kontrol.configure(state="normal")

    def proxy_ile_token_kontrol(self, token, random_proxy):
        self.thread_sayisi += 1
        try:
            r = httpx.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}, proxies={"http://":random_proxy, "https://":random_proxy}, timeout=5)
            if r.status_code == 200:
                console_token = token.split('.')
                self.kontrol_textbox.insert("0.0", f"GEÇERLİ     -     {console_token[0]}.{console_token[1]}.********************************************\n")
                with open("result/valid.txt","a") as f:
                    f.write(f"{token}\n")
                self.gecerli += 1
            elif r.status_code == 401:
                self.kontrol_textbox.insert("0.0", f"GEÇERSİZ -     {token}\n")
                with open("result/invalid.txt","a") as f:
                    f.write(f"{token}\n")
                self.gecersiz += 1
            elif r.status_code == 403:
                self.kontrol_textbox.insert("0.0", f"KİLİTLİ      -     {token}\n")
                with open("result/locked.txt","a") as f:
                    f.write(f"{token}\n")
                self.kilitli += 1
        except:
                self.kontrol_textbox.insert("0.0", f"HATA        -     Geçersiz Proxy :  {random_proxy} (5s içinde yanıt yok)\n")
                yeni_proxy = "http://" + random.choice(proxies_list).strip()
                self.proxy_ile_token_kontrol(token, yeni_proxy)
        self.thread_sayisi -= 1
        self.sayi += 1

    def github_ac(self):
        webbrowser.open(f"https://github.com/iseeuXD")

    def discord_ac(self):
        webbrowser.open(f"https://discord.gg/4zMQNuB3aZ")

    def website_ac(self):
        webbrowser.open(f"https://dev.prec.fun")

if __name__ == "__main__":
    AnaPencere()
