import tkinter as tk
from tkinter import messagebox
import time, threading, winsound, random, os
from datetime import datetime
from PIL import Image, ImageTk
from estructuras import DoublyLinkedList, Stack, Queue
from modelos import Alarm, TimeZone, Lap

CREEPY = {"bg": "#0a0000", "card": "#1a0505", "card2": "#2a0a0a", "text": "#cc0000",
          "text2": "#660000", "accent": "#ff0000", "green": "#00ff00", "red": "#ff0000",
          "blue": "#ff0000", "tab_bg": "#0d0000", "tab_inactive": "#550000",
          "divider": "#330000", "input_bg": "#1a0505", "white": "#e0d0d0"}

STATIC = {"bg": "#2a2a2a", "card": "#3a3333", "card2": "#4a3a3a", "text": "#cc0000",
          "text2": "#884444", "accent": "#bb0000", "green": "#aa0000", "red": "#ff0000",
          "blue": "#cc0000", "tab_bg": "#333333", "tab_inactive": "#665555",
          "divider": "#554444", "input_bg": "#3a3333", "white": "#d0c0c0"}

ZONES_DATA = [
    ("CDMX", "México", -6, "☠"), ("NYC", "EE.UU.", -5, "💀"),
    ("LA", "EE.UU.", -8, "👁"), ("London", "UK", 0, "🩸"),
    ("Madrid", "España", 1, "⚰"), ("Tokyo", "Japón", 9, "👻"),
    ("Shanghai", "China", 8, "🕷"), ("Sydney", "Australia", 10, "🦇"),
]

DAYS = ["LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"]
MONTHS = ["","ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]

GLITCH_CHARS = "̷̸̶̵̴̡̢̧̨̛̖̗̘̙̜̝̞̟̠̣̤̥̦̩̪̫̬̭̮̯̰̱̲̳̹̺̻̼"

def glitch(text):
    out = ""
    for ch in text:
        out += ch
        if random.random() < 0.3:
            out += random.choice(GLITCH_CHARS)
    return out

JEFF_IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jeff.png")

CREEPY_MSGS = [
    "G̷O̶ ̸T̵O̷ ̶S̸L̵E̴E̶P̸",
    "¿̷P̶u̸e̵d̷e̶s̸ ̵v̴e̵r̶m̸e̷?̸",
    "N̸o̷ ̶e̵s̸t̷á̶s̸ ̵s̴o̵l̶o̸",
    "D̷e̸t̵r̶á̷s̸ ̵d̶e̸ ̵t̷i̶.̸.̷.̶",
    "S̶o̷n̸r̵í̶e̷.̸.̶.̵",
]


class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("☠ R̷E̶L̸O̵J̷ ☠")
        self.root.geometry("400x720")
        self.root.resizable(False, False)

        self.alarm_list = DoublyLinkedList()
        self.alarm_queue = Queue()
        self.lap_stack = Stack()
        self.zones_array = [TimeZone(c, p, o, f) for c, p, o, f in ZONES_DATA]
        self.zone_nav = DoublyLinkedList()
        for z in self.zones_array:
            self.zone_nav.append(z)

        self.is_creepy = True
        self.t = CREEPY
        self.view = "clock"
        self.sw_running = False
        self.sw_start = 0
        self.sw_acc = 0
        self.sw_prev = 0
        self.lap_num = 0
        self.checked_min = -1
        self.glitch_on = True
        self.jeff_img = None
        self._load_jeff_image()

        self._build()
        self._show_clock()
        self._tick()
        self._check_alarms()
        self._glitch_loop()

    def _build(self):
        self.root.configure(bg=self.t["bg"])
        self.body = tk.Frame(self.root, bg=self.t["bg"])
        self.body.pack(fill="both", expand=True)

        self.tab_bar = tk.Frame(self.root, bg=self.t["tab_bg"], height=55)
        self.tab_bar.pack(fill="x", side="bottom")
        self.tab_bar.pack_propagate(False)

        self.tabs = {}
        icons = [("clock","💀\nReloj"),("alarm","🔔\nAlarma"),("stopwatch","⏱\nCrono"),("world","👁\nMundo")]
        for key, label in icons:
            b = tk.Button(self.tab_bar, text=label, font=("Courier New", 9, "bold"), bg=self.t["tab_bg"],
                          fg=self.t["tab_inactive"], bd=0, padx=6, pady=3, cursor="hand2",
                          activebackground=self.t["tab_bg"], command=lambda k=key: self._go(k))
            b.pack(side="left", expand=True, fill="both")
            self.tabs[key] = b

        self.theme_btn = tk.Button(self.tab_bar, text="👁", font=("Segoe UI", 13), bg=self.t["tab_bg"],
                                    fg=self.t["accent"], bd=0, cursor="hand2", command=self._toggle_theme)
        self.theme_btn.pack(side="right", padx=6)

    def _go(self, view):
        self.view = view
        for k, b in self.tabs.items():
            b.config(fg=self.t["accent"] if k == view else self.t["tab_inactive"])
        {"clock": self._show_clock, "alarm": self._show_alarms,
         "stopwatch": self._show_stopwatch, "world": self._show_world}[view]()

    def _clear(self):
        for w in self.body.winfo_children(): w.destroy()

    def _load_jeff_image(self):
        try:
            img = Image.open(JEFF_IMG_PATH)
            img = img.resize((160, 140), Image.NEAREST)
            self.jeff_img = ImageTk.PhotoImage(img)
        except:
            self.jeff_img = None

    def _toggle_theme(self):
        self.is_creepy = not self.is_creepy
        self.t = CREEPY if self.is_creepy else STATIC
        self.theme_btn.config(text="👁" if self.is_creepy else "📺")
        self.root.configure(bg=self.t["bg"])
        self.body.configure(bg=self.t["bg"])
        self.tab_bar.configure(bg=self.t["tab_bg"])
        for b in self.tabs.values(): b.configure(bg=self.t["tab_bg"])
        self.theme_btn.configure(bg=self.t["tab_bg"], fg=self.t["accent"])
        self._go(self.view)

    def _card(self, parent, **kw):
        return tk.Frame(parent, bg=self.t["card"], highlightbackground=self.t["divider"],
                        highlightthickness=1, **kw)

    def _glitch_loop(self):
        if self.view == "clock" and hasattr(self, "creepy_lbl"):
            try:
                self.creepy_lbl.config(text=random.choice(CREEPY_MSGS))
            except: pass
        self.root.after(random.randint(2000, 5000), self._glitch_loop)

    # ── CLOCK ──
    def _show_clock(self):
        self._clear()
        f = tk.Frame(self.body, bg=self.t["bg"])
        f.pack(expand=True)

        self.creepy_lbl = tk.Label(f, text=random.choice(CREEPY_MSGS),
                                    font=("Courier New", 10), bg=self.t["bg"], fg=self.t["text2"])
        self.creepy_lbl.pack(pady=(10,0))

        self.time_lbl = tk.Label(f, text="", font=("Courier New", 58, "bold"), bg=self.t["bg"], fg=self.t["accent"])
        self.time_lbl.pack(pady=(5,0))
        self.sec_lbl = tk.Label(f, text="", font=("Courier New", 24), bg=self.t["bg"], fg=self.t["text"])
        self.sec_lbl.pack()
        self.date_lbl = tk.Label(f, text="", font=("Courier New", 11), bg=self.t["bg"], fg=self.t["text2"])
        self.date_lbl.pack(pady=(2,8))

        if self.jeff_img:
            img_lbl = tk.Label(f, image=self.jeff_img, bg=self.t["bg"], bd=0)
            img_lbl.pack(pady=(0,5))
        else:
            tk.Label(f, text="👁  J̷E̶F̸F̵  👁", font=("Courier New", 14, "bold"),
                     bg=self.t["bg"], fg=self.t["text2"]).pack(pady=(0,5))

        row = tk.Frame(f, bg=self.t["bg"])
        row.pack(pady=5)
        for zone in self.zones_array[:3]:
            c = self._card(row)
            c.pack(side="left", padx=4, ipadx=10, ipady=6)
            tk.Label(c, text=zone.flag, font=("Segoe UI", 14), bg=self.t["card"]).pack()
            tk.Label(c, text=zone.city, font=("Courier New", 7, "bold"), bg=self.t["card"], fg=self.t["text2"]).pack()
            t = zone.get_time()
            tk.Label(c, text=t.strftime("%H:%M"), font=("Courier New", 13, "bold"), bg=self.t["card"], fg=self.t["text"]).pack()

        info = self._card(f)
        info.pack(fill="x", padx=30, pady=8, ipady=6)
        al = self.alarm_list.to_list()
        active = [a for a in al if a.active]
        txt = f"🔔 {len(active)} alarma(s) activa(s)" if active else "☠ Sin alarmas... por ahora"
        tk.Label(info, text=txt, font=("Courier New", 9), bg=self.t["card"], fg=self.t["text2"]).pack()

    def _tick(self):
        now = datetime.now()
        if self.view == "clock":
            try:
                self.time_lbl.config(text=now.strftime("%H:%M"), bg=self.t["bg"], fg=self.t["accent"])
                self.sec_lbl.config(text=now.strftime(":%S"), bg=self.t["bg"], fg=self.t["text"])
                self.date_lbl.config(text=f"☠ {DAYS[now.weekday()]} {now.day} {MONTHS[now.month]} {now.year} ☠",
                                     bg=self.t["bg"], fg=self.t["text2"])
            except: pass
        if self.view == "stopwatch" and self.sw_running:
            try:
                elapsed = self.sw_acc + (time.time() - self.sw_start)
                self.sw_lbl.config(text=Lap.format_time(elapsed))
            except: pass
        self.root.after(50, self._tick)

    # ── ALARMS ──
    def _show_alarms(self):
        self._clear()
        top = tk.Frame(self.body, bg=self.t["bg"])
        top.pack(fill="x", padx=20, pady=(15,5))
        tk.Label(top, text="🔔 A̷l̶a̸r̵m̷a̶s̸", font=("Courier New", 20, "bold"),
                 bg=self.t["bg"], fg=self.t["text"]).pack(side="left")

        form = self._card(self.body)
        form.pack(fill="x", padx=20, pady=8)
        r1 = tk.Frame(form, bg=self.t["card"])
        r1.pack(padx=10, pady=(8,4))
        tk.Label(r1, text="Hora", font=("Courier New", 9), bg=self.t["card"], fg=self.t["text2"]).pack(side="left")
        self.ah = tk.Spinbox(r1, from_=0, to=23, width=3, font=("Courier New", 14, "bold"), format="%02.0f",
                              bg=self.t["input_bg"], fg=self.t["accent"], bd=0, buttonbackground=self.t["card"])
        self.ah.pack(side="left", padx=3)
        tk.Label(r1, text=":", font=("Courier New", 14, "bold"), bg=self.t["card"], fg=self.t["accent"]).pack(side="left")
        self.am = tk.Spinbox(r1, from_=0, to=59, width=3, font=("Courier New", 14, "bold"), format="%02.0f",
                              bg=self.t["input_bg"], fg=self.t["accent"], bd=0, buttonbackground=self.t["card"])
        self.am.pack(side="left", padx=3)

        r2 = tk.Frame(form, bg=self.t["card"])
        r2.pack(padx=10, pady=(0,8), fill="x")
        self.an = tk.Entry(r2, font=("Courier New", 10), bg=self.t["input_bg"], fg=self.t["text"],
                           insertbackground=self.t["accent"], bd=0, width=18)
        self.an.insert(0, "despertar...")
        self.an.pack(side="left", padx=(0,6), ipady=3)
        tk.Button(r2, text="+ AGREGAR", font=("Courier New", 9, "bold"), bg=self.t["accent"], fg="#000",
                  bd=0, padx=10, pady=3, cursor="hand2", command=self._add_alarm).pack(side="right")

        self.alarm_box = tk.Frame(self.body, bg=self.t["bg"])
        self.alarm_box.pack(fill="both", expand=True, padx=20, pady=5)
        self._refresh_alarms()

    def _add_alarm(self):
        try:
            h, m = int(self.ah.get()), int(self.am.get())
            name = self.an.get().strip() or "Alarma"
        except: return
        if 0 <= h <= 23 and 0 <= m <= 59:
            a = Alarm(h, m, name)
            self.alarm_list.append(a)
            self.alarm_queue.enqueue(a)
            self._refresh_alarms()

    def _del_alarm(self, a):
        self.alarm_list.remove(a)
        self._refresh_alarms()

    def _tog_alarm(self, a):
        a.active = not a.active
        self._refresh_alarms()

    def _refresh_alarms(self):
        for w in self.alarm_box.winfo_children(): w.destroy()
        alarms = self.alarm_list.to_list()
        if not alarms:
            tk.Label(self.alarm_box, text="☠ No hay alarmas... dulces sueños ☠",
                     font=("Courier New", 10), bg=self.t["bg"], fg=self.t["text2"]).pack(pady=30)
            return
        for a in alarms:
            row = self._card(self.alarm_box)
            row.pack(fill="x", pady=3)
            inner = tk.Frame(row, bg=self.t["card"])
            inner.pack(fill="x", padx=10, pady=6)
            fg = self.t["accent"] if a.active else self.t["text2"]
            tk.Label(inner, text=a.time_str(), font=("Courier New", 20, "bold"), bg=self.t["card"], fg=fg).pack(side="left")
            tk.Label(inner, text=a.name, font=("Courier New", 9), bg=self.t["card"], fg=self.t["text2"]).pack(side="left", padx=6)
            tk.Button(inner, text="✕", font=("Courier New", 11), bg=self.t["card"], fg="#ff0000",
                      bd=0, cursor="hand2", command=lambda x=a: self._del_alarm(x)).pack(side="right")
            color = self.t["green"] if a.active else "#ff0000"
            tk.Button(inner, text="ON" if a.active else "OFF", font=("Courier New", 8, "bold"),
                      bg=self.t["input_bg"], fg=color, bd=0, padx=6, pady=2, cursor="hand2",
                      command=lambda x=a: self._tog_alarm(x)).pack(side="right", padx=4)

    def _check_alarms(self):
        now = datetime.now()
        h, m = now.hour, now.minute
        if m != self.checked_min:
            self.checked_min = m
            for a in self.alarm_list:
                if a.matches(h, m) and not a.ringing:
                    a.ringing = True
                    self._ring(a)
        self.root.after(1000, self._check_alarms)

    def _ring(self, a):
        def beep():
            for _ in range(5):
                try: winsound.Beep(800, 400)
                except: pass
                time.sleep(0.2)
            a.ringing = False
        threading.Thread(target=beep, daemon=True).start()
        messagebox.showinfo("☠ DESPIERTA", f"G̷O̶ ̸T̵O̷ ̶S̸L̵E̴E̶P̸\n\n{a.name}\n{a.time_str()}")

    # ── STOPWATCH ──
    def _show_stopwatch(self):
        self._clear()
        f = tk.Frame(self.body, bg=self.t["bg"])
        f.pack(expand=True, fill="both")
        tk.Label(f, text="⏱ C̷r̶o̸n̵ó̷m̶e̸t̵r̶o̷", font=("Courier New", 20, "bold"),
                 bg=self.t["bg"], fg=self.t["text"]).pack(pady=(12,5))

        elapsed = self.sw_acc + (time.time() - self.sw_start) if self.sw_running else self.sw_acc
        self.sw_lbl = tk.Label(f, text=Lap.format_time(elapsed), font=("Courier New", 46, "bold"),
                                bg=self.t["bg"], fg=self.t["accent"])
        self.sw_lbl.pack(pady=(5,8))

        btns = tk.Frame(f, bg=self.t["bg"])
        btns.pack(pady=6)
        color = "#ff0000" if self.sw_running else self.t["green"]
        txt = "⏸ PAUSA" if self.sw_running else "▶ INICIO"
        self.sw_btn = tk.Button(btns, text=txt, font=("Courier New", 11, "bold"), bg=color, fg="#000",
                                 bd=0, padx=18, pady=6, cursor="hand2", command=self._sw_toggle)
        self.sw_btn.pack(side="left", padx=3)
        tk.Button(btns, text="🏁 VUELTA", font=("Courier New", 10), bg=self.t["card"], fg=self.t["text"],
                  bd=0, padx=14, pady=6, cursor="hand2", command=self._sw_lap).pack(side="left", padx=3)
        tk.Button(btns, text="↺ RESET", font=("Courier New", 10), bg=self.t["card"], fg="#ff0000",
                  bd=0, padx=14, pady=6, cursor="hand2", command=self._sw_reset).pack(side="left", padx=3)

        self.lap_box = tk.Frame(f, bg=self.t["bg"])
        self.lap_box.pack(fill="both", expand=True, padx=20, pady=6)
        self._refresh_laps()

    def _sw_toggle(self):
        if self.sw_running:
            self.sw_acc += time.time() - self.sw_start
            self.sw_running = False
        else:
            self.sw_start = time.time()
            self.sw_running = True
        self._show_stopwatch()

    def _sw_lap(self):
        if not self.sw_running: return
        total = self.sw_acc + (time.time() - self.sw_start)
        self.lap_num += 1
        self.lap_stack.push(Lap(self.lap_num, total - self.sw_prev, total))
        self.sw_prev = total
        self._refresh_laps()

    def _sw_reset(self):
        self.sw_running = False
        self.sw_acc = 0
        self.sw_prev = 0
        self.lap_num = 0
        self.lap_stack.clear()
        self._show_stopwatch()

    def _refresh_laps(self):
        if not hasattr(self, "lap_box"): return
        for w in self.lap_box.winfo_children(): w.destroy()
        laps = self.lap_stack.to_list()
        if not laps:
            tk.Label(self.lap_box, text="☠ Registra vueltas... si te atreves",
                     font=("Courier New", 9), bg=self.t["bg"], fg=self.t["text2"]).pack(pady=10)
            return
        hdr = tk.Frame(self.lap_box, bg=self.t["bg"])
        hdr.pack(fill="x")
        for txt, w in [("#",6),("Vuelta",10),("Total",10)]:
            tk.Label(hdr, text=txt, font=("Courier New", 8, "bold"), bg=self.t["bg"], fg=self.t["text2"], width=w).pack(side="left")
        best = min(laps, key=lambda l: l.lap_time)
        worst = max(laps, key=lambda l: l.lap_time) if len(laps) > 1 else None
        for lap in laps:
            r = tk.Frame(self.lap_box, bg=self.t["card"])
            r.pack(fill="x", pady=1)
            fg = self.t["text"]
            if lap == best and len(laps) > 1: fg = self.t["green"]
            elif lap == worst: fg = "#ff0000"
            tk.Label(r, text=str(lap.number), font=("Courier New", 9), bg=self.t["card"], fg=fg, width=6).pack(side="left")
            tk.Label(r, text=Lap.format_time(lap.lap_time), font=("Courier New", 9), bg=self.t["card"], fg=fg, width=10).pack(side="left")
            tk.Label(r, text=Lap.format_time(lap.total_time), font=("Courier New", 9), bg=self.t["card"], fg=fg, width=10).pack(side="left")

    # ── WORLD ──
    def _show_world(self):
        self._clear()
        top = tk.Frame(self.body, bg=self.t["bg"])
        top.pack(fill="x", padx=20, pady=(15,5))
        tk.Label(top, text="👁 R̷e̶l̸o̵j̷ ̶M̸u̵n̶d̷i̸a̵l̶", font=("Courier New", 18, "bold"),
                 bg=self.t["bg"], fg=self.t["text"]).pack(side="left")
        nav = tk.Frame(top, bg=self.t["bg"])
        nav.pack(side="right")
        tk.Button(nav, text="◀", font=("Courier New", 12), bg=self.t["card"], fg=self.t["text"],
                  bd=0, padx=6, cursor="hand2", command=self._wp).pack(side="left", padx=2)
        tk.Button(nav, text="▶", font=("Courier New", 12), bg=self.t["card"], fg=self.t["text"],
                  bd=0, padx=6, cursor="hand2", command=self._wn).pack(side="left", padx=2)

        cur = self.zone_nav.get_current()
        if cur:
            hl = self._card(self.body)
            hl.pack(fill="x", padx=20, pady=8, ipady=10)
            t = cur.get_time()
            tk.Label(hl, text=f"{cur.flag}  {cur.city}", font=("Courier New", 14, "bold"),
                     bg=self.t["card"], fg=self.t["white"]).pack()
            tk.Label(hl, text=t.strftime("%H:%M:%S"), font=("Courier New", 32, "bold"),
                     bg=self.t["card"], fg=self.t["accent"]).pack()
            tk.Label(hl, text=f"{cur.country} • {cur.offset_str()}", font=("Courier New", 9),
                     bg=self.t["card"], fg=self.t["text2"]).pack()

        grid = tk.Frame(self.body, bg=self.t["bg"])
        grid.pack(fill="both", expand=True, padx=20, pady=5)
        for i, z in enumerate(self.zones_array):
            r, c = divmod(i, 4)
            cell = self._card(grid)
            cell.grid(row=r, column=c, padx=3, pady=3, sticky="nsew", ipadx=3, ipady=5)
            grid.columnconfigure(c, weight=1)
            t = z.get_time()
            sel = cur and z.city == cur.city
            fg = self.t["accent"] if sel else self.t["text"]
            tk.Label(cell, text=z.flag, font=("Segoe UI", 13), bg=self.t["card"]).pack()
            tk.Label(cell, text=z.city, font=("Courier New", 7, "bold"), bg=self.t["card"], fg=fg).pack()
            tk.Label(cell, text=t.strftime("%H:%M"), font=("Courier New", 12, "bold"), bg=self.t["card"], fg=fg).pack()

    def _wp(self):
        self.zone_nav.backward()
        self._show_world()

    def _wn(self):
        self.zone_nav.forward()
        self._show_world()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
