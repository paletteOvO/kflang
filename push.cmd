@echo off
cd C:\manhong\WorkSpace\Project\interp
git add .
git commit -m "Script commit at %DATE:~0,10% %TIME:~0,8% UTC+8"
git push --force