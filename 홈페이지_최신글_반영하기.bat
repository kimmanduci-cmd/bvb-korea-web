@echo off
chcp 65001 > nul
echo ========================================================
echo       [BVB KOREA] 홈페이지 최신 글 및 수정사항 반영
echo ========================================================
echo.
echo 1. 최신 작성된 기사 및 변경 파일을 수집합니다...
cd /d "%~dp0"

git add editorial_posts.json editorial_categories.json index.html assets/
git commit -m "Update: Editorial posts and site content (%date% %time%)"

echo.
echo 2. 웹 서버(Cloudflare / GitHub)로 안전하게 전송합니다...
git push origin main

echo.
echo ========================================================
echo  [반영 완료!]
echo  최신 글과 사진이 웹사이트로 성공적으로 전송되었습니다.
echo  약 15~30초 후 실제 도메인(bvbkorea.co.kr)에 자동 반영됩니다.
echo ========================================================
echo.
pause
