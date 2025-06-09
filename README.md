[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

# MUMS Food Reservation

A simple desktop application for automating meal reservations on the MUMS (Mashhad University of Medical Sciences) student food reservation portal.

## Features

* Login with username, password and CAPTCHA support
* Navigate through weeks and select meal type (breakfast, lunch, dinner, etc.)
* Select cafeteria and view available menus
* Automate final reservation and refresh UI to reflect reserved meals

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/essu-food-reservation.git
   cd essu-food-reservation
   ```

2. **Create a Python virtual environment** (optional but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows use `venv\\Scripts\\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Tkinter setup**

   * **macOS:**

     ```bash
     brew install python-tk
     ```

     On newer macOS versions, you may need to install the `python-tk` formula or use the official Python installer from python.org which bundles Tkinter.

   * **Linux (Debian/Ubuntu):**

     ```bash
     sudo apt-get install python3-tk
     ```

   * **Windows:** Tkinter is included by default with the standard Python installer. If you encounter issues, reinstall Python from [python.org](https://www.python.org/) and ensure "tcl/tk and IDLE" is checked.

## Usage

```bash
python main.py
```

* Enter your MUMS credentials and CAPTCHA
* Use the UI to navigate weeks and select meals
* Upon reservation, the interface will auto-refresh to show your booked meal

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.