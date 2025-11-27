# Password-strength-and-cracker-Educational-purpose-
This is a project for my college and in this project we test the strength of password and also crack the password that we enter by using Brute-force and Dictionary attack
🛡️ ADVANCED CYBER SECURITY AUDITOR v3.0

This application is a Python tool built using Tkinter for academic study of password security and attack vectors. It provides a custom, dark-themed graphical user interface with two main functional tabs.

🚀 Application Summary

1. 🔐 STRENGTH AUDIT (Password Entropy Analyzer)

This section provides real-time analysis of any entered password. The strength score (out of 100) is calculated based on a weighted formula that highly rewards password length and character diversity (uppercase, numbers, symbols, etc.). It applies significant penalties if the password is too short, lacks diversity, or contains common dictionary words or predictable character patterns (like 1234 or aaa). The user receives instant visual feedback via a progress bar and detailed, actionable suggestions for improving the password's security.

2. 🎯 PASSWORD CRACK SIMULATION

This tab demonstrates the vulnerability of passwords by simulating common attack techniques. It uses a separate thread to run the simulation, preventing the GUI from freezing.

Dictionary Attack: The simulation quickly tests the target password against a small, built-in list of extremely common and weak credentials.

Brute Force Attack: This tests the target against every possible combination of letters and digits for a selected length (5, 6, or 8 characters). This vividly illustrates why short passwords are computationally weak.

💻 Installation and Execution

The application is highly portable and requires Python 3.x and the standard Tkinter library.

To run the application:

Save the code as Password crack and Strength tester.py.

Open your terminal in the file's directory.

Execute using the command: python "Password crack and Strength tester.py"
