#!/bin/sh

echo 'Starting dev script'

server() {
  while true; do
    COUNTER=0
    COUNTER_BASE=0
    while true; do
      RESTART=$(cat <> "restart-pipe" < "restart-pipe")
      if [ -n "$RESTART" ]; then
        COUNTER=$(($COUNTER + 1))
      fi

      if [ "$COUNTER" != "$COUNTER_BASE" ]; then
        COUNTER_BASE=$COUNTER
      else
        break
      fi
    done

    if [ $COUNTER != "0" ]; then
      pushd /app
      echo 'Restarting'
      npm start > /var/log/dev.log &
      popd
    fi

    sleep 5
  done
}

listener() {
  while inotifywait -e modify -e create -e delete /app; do
    echo '1' > restart-pipe
  done
}

mkfifo restart-pipe
echo '1' > restart-pipe &
listener &
server
