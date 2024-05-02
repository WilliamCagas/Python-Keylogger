# Python-Keylogger

Note: This project was created for EDUCATIONAL PURPOSES only. 

A keylogger is a surveillance software that can log every pressed key from a computer. It can be used to gather information. My end goal was to explore the world of cybersecurity by creating a functional keylogger program using Python that could log my own data and send it to my email.


For Use (needs a gmail account with 2FA enabled):
1. Go into 2FA settings of the gmail account.
2. Look for and create an app password.
3. Paste the app password into the string for the self.SENDER_PASS variable.
4. Type the email address into the string for the self.SENDER variable.

Features:
- Keystroke logs with timestamps
- Geolocation data using external APIs (IP, ISP, City, Country, etc.)
- Screenshots using pyautogui
- Reports using .txt files (creates detailed reports while uses temporary directories)
- SMTP handling with Gmail, creating/sending emails and providing attachments
- Threading
