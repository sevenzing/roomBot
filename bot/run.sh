#!/bin/bash

echo_and_log()
{
  message=$1
  # to console
  echo $message 
  # to log file
  echo "$(date '+%Y-%m-%d %H:%M:%S') | run.sh script |" $message >> roomBot.log
  # to telegram
  python run.py --send-message "${message}"
}


echo_and_log "Starting bot"
python -u run.py --start
result=$?

time_start=$(($(date +%s%N)/1000000000)) # IN SECONDS 
flag=0

# While true
while [ ${result} != -1 ]; do
    echo_and_log "Got exit code ${result}. Restarting bot in 10 seconds"
    sleep 10
    echo_and_log "Starting bot"
    python -u run.py --start
    result=$?
    time_finished=$(($(date +%s%N)/1000000000)) # IN SECONDS 

    if [ ${result} -eq 137 ]; then # If exited with fucking telegram exception
        # just restart 

        amount_to_sleep=`expr 120 - ${time_finished} + ${time_start}`
        
        amount_to_sleep=$((amount_to_sleep>0 ? amount_to_sleep : 5))

        echo_and_log "Telegram error 137: Sleep in ${amount_to_sleep} seconds"

        sleep ${amount_to_sleep}

    fi
    
    time_start=${time_finished}
done


echo_and_log "Bot exited with code ${result}. ALERT! bot stopped."
exit $result
