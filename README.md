# Python-Keylogger

Note: This project was created for EDUCATIONAL PURPOSES only. It demonstrates how keyloggers work and explores various related concepts, including system monitoring, data capture, and email reporting.


		
Purpose: A keylogger is a surveillance software that can log every pressed key from a computer. My goal was to explore the world of cybersecurity and gain experience by creating a real-world scenario in a controlled environment. To do this, I created a functional keylogger program using Python that could track my own data and send it to my email.

Disclaimer: The creator of this project does not endorse or condone any unauthorized or malicious use of keylogging technology. Users are encouraged to use this project responsibly, in compliance with applicable laws and ethical guidelines.

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
