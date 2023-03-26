###########################
## Initial Configuration ##
###########################

src_slurm_helper="/private/home/chaoyizhang/ebatch"
CKPT_DIR='/checkpoint/chaoyizhang/projectX'







##########################
## General SLURM Command #
##########################

#alias check_all_jobs='squeue -o            "%.8Q %.10i %.3P %.9j %.6u %.2t %.16S %.10M %.10l %.5D %.12b %.2c %.4m %R" -S -t,-p,i | less -N '
#alias check_my_squeue="squeue -u $USER"

alias check='squeue --iterate 1 -u  $USER -o      "%.5i %.8Q %.3P %.15j %.6u %.11T %.10M %.5D %.4C %.13b %R" -S -t,-p,i'  # %.10l (time_limit) %.2t (status) %.16S (start_time) %.10m(min_memory)
alias checkjob='squeue --iterate 1 -o             "%.5i %.8Q %.3P %.15j %.6u %.11T %.10M %.5D %.4C %.13b %R" -S -t,-p,i'
alias checknode="sinfo -t idle,mixed -Node -p gpu -o '%20N %.5T %.3c %.9z %.7m %.7e %.7w %.80f'"

alias cj='scancel '                 # cancel one particular job (usage: +job_id)
alias cj_all='scancel -u $USER'     # cancel all job
alias sj='scontrol show jobid -dd ' # show   one particular job (usage: +job_id)
#alias mj='squeue -u $USER -o   "%.8Q %.10i %.3P %.9j %.6u %.2t %.16S %.10M %.10l %.5D %.12b %.2c %.4m %R" -S -t,-p,i | less -N '
rj(){scontrol update jobid "${1}" jobname "${2}"}


#########################
##    easy sbatch      ##
#########################
alias ebatch="clear; python $src_slurm_helper/ebatch_run.py"
elaunch(){clear; chmod 777 "$@"; "$@";} 
mj(){tail -f --retry -n 20 $CKPT_DIR/slurm_logs/ebatch."$@".out}             
echeck(){echo "\n\n\n"; cat $CKPT_DIR/slurm_logs/ebatch."$@".slurm}   
elogin(){srun --jobid="$@" --pty zsh} 




