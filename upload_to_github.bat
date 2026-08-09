@echo off
echo ========================================================
echo GITHUB PUSH SCRIPT FOR STREAMLIT CLOUD DEPLOYMENT
echo ========================================================
echo.
git add .
git commit -m "Deploy Streamlit Chatbot with Rosegold layout"

echo Pushing fix to GitHub...
git push -u origin main --force

echo.
echo ========================================================
echo SUCCESS! Your code has been pushed to GitHub.
echo Streamlit Cloud will now automatically rebuild and start!
echo ========================================================
pause
