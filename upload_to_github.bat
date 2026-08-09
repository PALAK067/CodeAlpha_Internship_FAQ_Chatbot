@echo off
echo ========================================================
echo GITHUB UPLOAD SCRIPT FOR CODEALPHA TASK 2
echo ========================================================
echo.
echo Initializing Git repository...
git init

echo Adding files...
git add .

echo Committing...
git commit -m "CodeAlpha Task 2: FAQ Chatbot implementation with Rosegold theme and Emojis"

echo Setting up remote...
git remote add origin https://github.com/PALAK067/CodeAlpha_Internship_FAQ_Chatbot.git
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================================
echo If you saw a login popup, please log in.
echo If it says "Everything up-to-date" or "branch main set up to track", you are good!
echo ========================================================
pause
