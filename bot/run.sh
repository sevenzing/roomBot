#!/bin/bash

echo_and_log()
{
  message=$1
  echo $message
  echo "$(date '+%Y-%m-%d %H:%M:%S') | run.sh script |" $message >> roomBot.log
}


echo_and_log "Starting bot"
python -u run.py
result=$?

time_start=$(($(date +%s%N)/1000000))
flag=0
while [ ${result} != 0 ]; do
    echo_and_log "Got exit code 1"
    echo_and_log "Restarting bot in 5 seconds"
    sleep 5

    python -u run.py
    result=$?
    time_finished=$(($(date +%s%N)/1000000))

    if [ ${result} -eq 137 ]; then # If exited with fucking telegram exception
        # just restart 
        sleep 10
        time_start=${time_finished}
        continue
    fi

    if [ `expr ${time_finished} - ${time_start}` -lt 30000 ]; then
        if [ ${flag} -eq 1 ]; then
          break
        fi

        echo_and_log "restart in less than 30 seconds. sleep for 1 minute"
        flag=1
        sleep 60
    else
      flag=0
    fi
    
    time_start=${time_finished}
done


echo_and_log "Bot exited with code ${result}"
exit $result
