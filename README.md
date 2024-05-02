# Python-Keylogger

Note: This project was created for EDUCATIONAL PURPOSES only. It demonstrates how keyloggers work and explores various related concepts, including system monitoring, data capture, and email reporting.
		
Purpose: A keylogger is a surveillance software that can log every pressed key from a computer. My goal was to explore the world of cybersecurity and gain experience by creating a real-world, malicious software (malware) in a controlled environment. To achieve this, I created a functional keylogger program using Python that can track user keystrokes and send the logged data via email.

Disclaimer: The creator of this project does not endorse or condone any unauthorized or malicious use of keylogging technology. Users are encouraged to use this project responsibly, in compliance with applicable laws and ethical guidelines.

For gmail security purposes, a gmail account must have Two-Factor Authentication enabled for use.

For Use:
1. Find the 2FA settings of the gmail account.
2. In these settings, search for and create an "App Password".
3. Copy and paste the app password into the string for the self.SENDER_PASS variable.
4. Copy and paste the email address into the string for the self.SENDER variable.

Features:
- Keystroke logs with timestamps
- Geolocation data using external APIs (IP, ISP, City, Country, etc.)
- Screenshots using pyautogui
- Reports using .txt files (creates detailed reports while uses temporary directories)
- SMTP handling with Gmail, creating/sending emails and providing attachments
