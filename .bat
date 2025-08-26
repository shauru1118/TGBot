@echo off

IF "%1" EQU "docker" (
    echo ================
    echo Docker : DOING
    docker build . -t shauru1118/tgbot-py
    echo =
    echo Docker : build DONE
    echo =
    docker push shauru1118/tgbot-py
    echo =
    echo Docker : push DONE
    echo =
    echo Docker : DONE
    echo ================    
)

IF "%1" EQU "git" (
    echo ================
    echo Git : DOING
    git add .
    git commit -m "%2"
    echo =
    echo Git : commit DONE
    echo =
    git push origin main
    echo =
    echo Git : push DONE
    echo =
    echo Git : DONE
    echo ================
)

IF "%1" EQU "all" (
    echo ================
    echo Git : DOING
    git add .
    git commit -m "%2"
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
    docker build . -t shauru1118/tgbot-py
    echo =
    echo Docker : build DONE
    echo =
    docker push shauru1118/tgbot-py
    echo =
    echo Docker : push DONE
    echo =
    echo Docker : DONE
    echo ================    
)
