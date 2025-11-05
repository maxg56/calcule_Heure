@echo off
REM Script de lancement pour Windows

echo 🚀 Démarrage de l'application de gestion des horaires...
echo.

REM Vérifier si streamlit est installé
where streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Streamlit n'est pas installé. Installation en cours...
    pip install -r requirements.txt
)

REM Lancer l'application
echo 📊 Ouverture de l'application web...
streamlit run app.py
