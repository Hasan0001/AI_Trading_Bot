import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from data import make_client, fetch_klines
from indicators import add_indicators
from trading_bot import AdvancedTradingBot
from config import settings


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Crypto Bot — Binance")
        self.geometry("1100x750")
        self.configure(bg="#0b0f14")  # dark web3 vibe

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#0b0f14", foreground="#e2e8f0")
        self.style.configure("TButton", padding=6, relief="flat", background="#111827", foreground="#cbd5e1")
        self.style.map("TButton", background=[("active", "#1f2937")])
        self.style.configure("TLabelframe", background="#0b0f14", foreground="#93c5fd")
        self.style.configure("TLabelframe.Label", background="#0b0f14", foreground="#93c5fd")

        self._build_config()
        self._build_controls()
        self._build_status()
        self._build_chart()
        self._build_log()

        self.bot = AdvancedTradingBot(gui_callback=self.on_bot_event)
        self.after(1000, self.refresh_chart)

    def _build_config(self):
        frm = ttk.LabelFrame(self, text="Configuration")
        frm.place(x=20, y=20, width=350, height=260)

        ttk.Label(frm, text="API Key").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.api_key = ttk.Entry(frm, show="*")
        self.api_key.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(frm, text="API Secret").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.api_secret = ttk.Entry(frm, show="*")
        self.api_secret.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(frm, text="Mode").grid(row=2, column=0, sticky="w", padx=6, pady=4)
        self.mode = ttk.Combobox(frm, values=["Paper", "Real"])
        self.mode.current(0)
        self.mode.grid(row=2, column=1, padx=6, pady=4)

        ttk.Label(frm, text="Model").grid(row=3, column=0, sticky="w", padx=6, pady=4)
        self.model = ttk.Combobox(frm, values=["RF", "NN"])
        self.model.current(0)
        self.model.grid(row=3, column=1, padx=6, pady=4)

        ttk.Label(frm, text="Budget per Trade (USDT)").grid(row=4, column=0, sticky="w", padx=6, pady=4)
        self.budget = ttk.Entry(frm)
        self.budget.insert(0, "50")
        self.budget.grid(row=4, column=1, padx=6, pady=4)

        ttk.Label(frm, text="Pair").grid(row=5, column=0, sticky="w", padx=6, pady=4)
        self.pair = ttk.Combobox(frm, values=["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT"])
        self.pair.current(0)
        self.pair.grid(row=5, column=1, padx=6, pady=4)

    def _build_controls(self):
        frm = ttk.LabelFrame(self, text="Controls")
        frm.place(x=20, y=300, width=350, height=150)

        self.btn_start = ttk.Button(frm, text="Start Bot", command=self.start_bot)
        self.btn_start.grid(row=0, column=0, padx=8, pady=10)

        self.btn_stop = ttk.Button(frm, text="Stop Bot", command=self.stop_bot)
        self.btn_stop.grid(row=0, column=1, padx=8, pady=10)

        self.btn_train = ttk.Button(frm, text="Train Now", command=self.train_now)
        self.btn_train.grid(row=1, column=0, padx=8, pady=10)

        self.btn_save = ttk.Button(frm, text="Save Model", command=self.save_model)
        self.btn_save.grid(row=1, column=1, padx=8, pady=10)

    def _build_status(self):
        frm = ttk.LabelFrame(self, text="Status")
        frm.place(x=20, y=470, width=350, height=180)

        self.lbl_conn = ttk.Label(frm, text="Connection: Unknown")
        self.lbl_conn.pack(anchor="w", padx=8, pady=4)

        self.lbl_balance = ttk.Label(frm, text="Balance: —")
        self.lbl_balance.pack(anchor="w", padx=8, pady=4)

        self.lbl_model = ttk.Label(frm, text="Model: RF (ready)")
        self.lbl_model.pack(anchor="w", padx=8, pady=4)

        self.lbl_strategy = ttk.Label(frm, text="Active Strategy: —")
        self.lbl_strategy.pack(anchor="w", padx=8, pady=4)

        self.lbl_perf = ttk.Label(frm, text="Equity: — | DD: — | Sharpe: —")
        self.lbl_perf.pack(anchor="w", padx=8, pady=4)

    def _build_chart(self):
        frm = ttk.LabelFrame(self, text="Chart")
        frm.place(x=390, y=20, width=690, height=480)

        self.figure = Figure(figsize=(6.4, 4.2), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=frm)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_log(self):
        frm = ttk.LabelFrame(self, text="Activity Log")
        frm.place(x=390, y=520, width=690, height=200)

        self.log = tk.Text(frm, bg="#0b1220", fg="#a5b4fc")
        self.log.pack(fill="both", expand=True)

    def append_log(self, text):
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def on_bot_event(self, event):
        t = event.get("type")
        if t == "status":
            self.append_log(event.get("message", ""))
        elif t == "metrics":
            self.lbl_strategy.config(text=f"Active Strategy: {event['strategy']}")
            self.lbl_perf.config(
                text=f"Equity: {event['equity']:.2f} | DD: {event['drawdown']:.2%} | Sharpe: {event['sharpe']:.2f}"
            )

    def start_bot(self):
        try:
            budget = float(self.budget.get())
        except ValueError:
            messagebox.showerror("Invalid budget", "Enter a valid number for budget.")
            return

        paper = (self.mode.get() == "Paper")
        api_key = self.api_key.get().strip()
        api_secret = self.api_secret.get().strip()

        self.bot.configure(self.pair.get(), paper, self.model.get(), budget, api_key, api_secret)
        self.bot.start()
        self.append_log("Bot started.")

    def stop_bot(self):
        self.bot.stop()
        self.append_log("Bot stopped.")

    def train_now(self):
        self.append_log("Manual training requested — will retrain on next loop.")

    def save_model(self):
        try:
            path = f"models_store/{self.model.get().lower()}_latest"
            self.bot.model_mgr.save(path)
            self.append_log(f"Model saved to {path}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))

    def refresh_chart(self):
        try:
            client = make_client(self.api_key.get().strip(), self.api_secret.get().strip(), self.mode.get() == "Paper")
            df = fetch_klines(client, self.pair.get(), settings.interval, limit=210)
            if df is not None:
                df = add_indicators(df)
                self.ax.clear()
                self.ax.plot(df.index, df["close"], label="Close")
                self.ax.plot(df.index, df["sma_10"], label="SMA10")
                self.ax.plot(df.index, df["sma_30"], label="SMA30")
                self.ax.legend(loc="upper left")
                self.ax.set_title(self.pair.get())
                self.canvas.draw()
                self.lbl_conn.config(text="Connection: OK")
        except Exception:
            self.lbl_conn.config(text="Connection: Error")
        finally:
            self.after(5000, self.refresh_chart)
