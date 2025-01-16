rm -rf log
rm -rf results


execute the command
servers="172.16.240.95 14.225.238.8"
ports="6377 6378 6379"
measure=3
# connection=100
# number=100
connections="10"
numbers="3"
ratios="1:1"

# Nested for loops
for server in $servers; do
    for port in $ports; do
        for ratio in $ratios; do
            for connection in $connections; do
                for number in $numbers; do
                    command="python3 main.py --server=$server --port=$port --ratio=$ratio --measure=$measure --connection=$connection --number=$number"
                    eval $command
                done
            done
        done
    done
done