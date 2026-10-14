@echo off
chcp 65001 > nul
echo ========================================================
echo       [BVB KOREA] 홈페이지 글쓰기 및 편집 모드 실행
echo ========================================================
echo.
echo 로컬 편집 서버를 실행하고 브라우저를 엽니다...
cd /d "%~dp0"

start http://localhost:8080
python server.py

pause
