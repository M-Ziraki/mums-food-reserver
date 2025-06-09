import tkinter as tk
from gui import ESSAuthenticationApp, ESSReserveApp


def start_reservation(session):
    """پس از موفقیت در لاگین، پنجرهٔ رزرو را باز می‌کند."""
    res_root = tk.Tk()
    ESSReserveApp(res_root, session)
    res_root.mainloop()


def main():
    root = tk.Tk()
    ESSAuthenticationApp(root, on_success=start_reservation)
    root.mainloop()


if __name__ == '__main__':
    main()
