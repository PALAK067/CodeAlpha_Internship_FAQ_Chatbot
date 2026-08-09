@echo off
echo ========================================================
echo GITHUB OVERWRITE SCRIPT FOR CODEALPHA TASK 2
echo ========================================================
echo.
echo Committing the Gradio version...
git add .
git commit -m "Restoring final Gradio Version"

echo Forcefully pushing to GitHub...
git push -u origin main --force

echo.
echo ========================================================
echo Done! Your GitHub has been forcefully overwritten with the original Gradio version.
echo ========================================================
pause
