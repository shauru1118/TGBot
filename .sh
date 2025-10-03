echo ================
echo Git : DOING
git add .
git commit -m "%1"
echo =
echo Git : commit DONE
echo =
git push origin main
echo =
echo Git : push DONE
echo =
echo Git : DONE
echo ================

echo =
echo =
echo =
echo =

echo ================
echo Docker : DOING
sudo docker build . -t shauru1118/new-tgbot
echo =
echo Docker : build DONE
echo =
sudo docker push shauru1118/new-tgbot:latest
echo =
echo Docker : push DONE
echo =
echo Docker : DONE
echo ================
