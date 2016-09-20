find . -type f -name "initiate" -exec echo \#{} \; -exec grep "nohup" {} \; -exec echo sleep 1 \; -exec echo \; > dump
