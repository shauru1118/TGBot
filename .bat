@echo off

echo ================
echo Git : DOING
git add .
git commit -m "%1"
git push origin main
echo Git : DONE
echo ================

echo 
echo ================
echo Docker : DOING
docker build . -t shauru1118/tgbot-py
docker push shauru1118/tgbot-py
echo Docker : DONE
