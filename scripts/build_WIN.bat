del /q *.pyz

xcopy /s/e/i "../game" "../wrapper/game"
python -m zipapp "../wrapper" -o "../br_launcher.pyz"
del /q/s "../wrapper/game"