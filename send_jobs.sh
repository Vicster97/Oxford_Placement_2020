#!/bin/bash

nRuns=3 # number of arrays that I want to submit at once (dont exceed 5,000 or the jobs will be requeued)
start=1 # first array
end=$(( $start + $nRuns -1 )) # last array

runIdOffset=0 # packs arrays in jobs of 1000 arrays

for (( i=$start; i<=$end; i++ )); do
        echo "Array number $i"
        if [[ $i -eq $start ]] || [[ `expr $i % 1000` -eq 0 ]]; then # If $i is our first array, or $i is our 1000 array (i.e. modulo = 0), submit a job of 1000 arrays max.
                if [[ $nRuns -gt 999 ]]; then
                        echo "Submit a job of 1000 arrays, with runs from `expr $runIdOffset + 1` to `expr $runIdOffset + 1000`"
                fi
                sbatch --export=OFFSET=$runIdOffset run_models.sh  # pass the command line variable runIdOffset to the submission script
                runIdOffset=$(($runIdOffset + 1000)) # update runIdOffset
                echo "Run ID offset is $runIdOffset"
        fi
done

