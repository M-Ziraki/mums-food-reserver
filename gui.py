import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from io import BytesIO
from bs4 import BeautifulSoup

from auth import ESSSession
from reservation import fetch_page, parse_panels


class ESSAuthenticationApp:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.session = ESSSession()
        self._build_ui()
        self._load_captcha()

    def _build_ui(self):
        self.root.title("ESSU Login")
        tk.Label(self.root, text="Username:").grid(row=0, column=0, sticky='e')
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, sticky='e')
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)
        tk.Label(self.root, text="Captcha:").grid(row=2, column=0)
        self.captcha_panel = tk.Label(self.root)
        self.captcha_panel.grid(row=2, column=1)
        self.captcha_entry = tk.Entry(self.root)
        self.captcha_entry.grid(row=3, column=1, pady=5)
        tk.Button(self.root, text="Reload Captcha",
                  command=self._load_captcha).grid(row=4, column=0)
        tk.Button(self.root, text="Login",
                  command=self._login).grid(row=4, column=1)

    def _load_captcha(self):
        try:
            data = self.session.load_captcha()
            img = Image.open(BytesIO(data))
            self.captcha_img = ImageTk.PhotoImage(img)
            self.captcha_panel.config(image=self.captcha_img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load captcha:\n{e}")

    def _login(self):
        try:
            result = self.session.login(
                self.username_entry.get(),
                self.password_entry.get(),
                self.captcha_entry.get()
            )
            if not result.get('Key'):
                messagebox.showwarning(
                    "Login Failed", result.get('Value', 'Unknown error'))
                self._load_captcha()
            else:
                self.root.destroy()
                self.on_success(self.session)
        except Exception as e:
            messagebox.showerror("Error", f"Login error:\n{e}")
            self._load_captcha()


class ESSReserveApp:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        self.root.title("ESSU Food Reservation")
        self.last_html = ""
        self._build_ui()
        self._fetch()

    def _build_ui(self):
        nav = tk.Frame(self.root)
        nav.pack(pady=5)
        tk.Button(nav, text="<< Prev Week",
                  command=lambda: self._fetch('prev')).pack(side='left')
        tk.Button(nav, text="Today", command=lambda: self._fetch(
            'today')).pack(side='left')
        tk.Button(nav, text="Next Week >>",
                  command=lambda: self._fetch('next')).pack(side='left')

        mframe = tk.Frame(self.root)
        mframe.pack(pady=5)
        tk.Label(mframe, text="Meal:").pack(side='left')
        self.meal_var = tk.StringVar()
        self.meal_dd = ttk.Combobox(
            mframe, textvariable=self.meal_var, state='readonly')
        self.meal_dd.pack(side='left')
        self.meal_dd.bind('<<ComboboxSelected>>',
                          lambda e: self._fetch('meal'))

        self.days_frame = tk.Frame(self.root)
        self.days_frame.pack(fill='both', expand=True)

    def _fetch(self, action=None):
        try:
            meal_val = None
            if action == 'meal':
                # مقدار value وعده انتخابی
                soup0 = BeautifulSoup(self.last_html, 'html.parser')
                sel0 = soup0.find(id='body_dpFoodMeal')
                for o in sel0.find_all('option'):
                    if o.text == self.meal_var.get():
                        meal_val = o['value']
                        break
            self.last_html = fetch_page(
                self.session, self.last_html, action, meal_val)
            panels = parse_panels(self.last_html)
            self._render_panels(panels)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to fetch page:\n{e}")

    def _render_panels(self, panels):
        for w in self.days_frame.winfo_children():
            w.destroy()
        for idx, info in enumerate(panels):
            panel = tk.LabelFrame(self.days_frame, text=info['title'])
            panel.grid(row=idx//3, column=idx %
                       3, padx=5, pady=5, sticky='nsew')
            if info['reserved_label']:
                tk.Label(panel, text=f"✅ رزرو شده: {info['reserved_label']}").pack(
                    fill='x', padx=5, pady=10)
            elif info['caf_options']:
                var = tk.StringVar()
                cb = ttk.Combobox(panel, textvariable=var, values=[
                                  t for t, _ in info['caf_options']], state='readonly')
                cb.pack(fill='x', padx=5)
                cb.bind('<<ComboboxSelected>>', lambda e, i=idx,
                        v=var: self._on_cafeteria(i, v.get(), info['caf_options']))
        for c in range(3):
            self.days_frame.columnconfigure(c, weight=1)

    def _on_cafeteria(self, day, text, caf_options):
        # پس از انتخاب سلف، منو بارگذاری و دیالوگ انتخاب غذا را باز می‌کند
        from reservation import fetch_page, parse_panels
        # ... (می‌توانید این بخش را مشابه on_cafeteria_select پیاده کنید)
        pass  # برای اختصار
