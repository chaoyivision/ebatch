# ebatch for SLURM
easy_sbatch tools for any slurm cluster.


### Usage
**simply adding one word `ebatch` to make a local command runnable with sbatch (i.e., launch it w/ ANY SLURM cluster).**

As for *FAIR coolcats[0]*...
* suppose you tested &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  `python train.py --args....` on *devfair*, 
* then now simply type `ebatch "python train.py --args...."` to launch it with sbatch on *learnfair*.


### To install it
1. `git clone https://github.com/chaoyivision/ebatch.git` and open it.
2. change `register2cml.zsh`:
   * change its 1st variable (i.e., `src_slurm_helper`) to its current position (i.e., `pwd`).
   * change its 2nd variable (i.e., `CKPT_DIR`) to your desired CKPT position (i.e., it should be as same as `CKPT_DIR` in `ebatch_cfg.py` below).
4. add `source [path_to_it]/register2cml.zsh` in your `~/.zshrc`  (or `~/.bashrc`), and restart the terminal.
5. `pip install Random-Word` (there might be other packages required... pls. forgive me for being lazy :D )

### To config it
change setting in `ebatch_cfg.py` (explained as below).

### To test it
try `ebatch "echo Hello FAIR"`


# ebatch
* ebatch_cfg.py (configuration of ebatch)
```
CKPT_DIR =           '/checkpoint/USER_NAME/projectXckpt'
LOCAL_CODEBASE =     '/private/home/USER_NAME/REPO/projectX'     # where snapshot will be taken
PREPARING_COMMANDS = 'source ~/.bashrc; conda activate envX; pwd;' 
DEFAULT_PARTITION =  'pixar'
```
`PREPARING_COMMANDS` is always execauted before running your own command (such as, activate conda env and etc).

You can also make them changable with args.parser(), to run arbitary codebase (`LOCAL_CODEBASE`) and save at arbitary position (`CKPT_DIR`). For current version, since they are mostly unchanged during our development of one project, I just put them here for being lazy.

* **CommondLine** (within Terminal)
    * **ebatch**: easy_sbatch for [command]
        * `ebatch --help`
        * `ebatch [commond] [-J job_name] [-p partition] [-G ngpus]`
        * if you do not frequently change partition or ngpus (i.e., setting them either in ebatch_cfg.py or ebatch_run.py)
            * suppose your local training command is &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python train.py --args`
            * **you simply add one word ahead:** `ebatch "python train.py --args"` **to launch it with sbatch**
            * or set custom job_name as:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `ebtach "python train.py --args" -J myJobName`
    * **elaunch**: launch a script of ebatch_works
        * suppoe xxx.zsh contains several lines of ebatch commands, for example, 
        ```
         #!/usr/bin/zsh
         source ~/.zshrc # (or ~/.bashrc) -> this line is important to load ebatch-alias
         
         ebatch "commandA" -J taskA;
         ebatch "commandB" -J taskB;
         ebatch "commandC" -J taskC
        ```
        * `elaunch  xxx.zsh` to launch these jobs parallelly to the cluster.
    * **elogin**: ssh into a specific node with jobid
        * `elogin [jobid]` 
        * once logged-in, you can interact with it (for example, using nvidia-smi to check current gpu usage).
    * **echeck**: show sbatch script of jobid              (launched by ebatch)
        * `echeck [jobid]`
    * **mj**:      monitor progress of jobid    (launched by ebatch)
        * `mj [jobid]`

* Note:
    * two folders will be created under `CKPT_DIR`, to (1) save slurm.out and slurm_config, and (2) to snapshoot current codebase 
    * `--nodes=1` is not used in this script. And one benefit is that you can ask more than 8 gpus, for example, try with `-G 32`, the slurm manager would take care of the multi-node setting, and fetch you 32 gpus across multiple nodes. If you'd like, you can manually add this constraint back into `ebatch_run.py`.
    * **job failed due to code changes (while it's pending)?** At each time when `ebatch` is invoked, we take a snapshoot of current codebase (in case we might change the codebase while the job is pending for minutes or even hours) and run experiments on this copied codebase when job is eventually schedualled.
    
# SLRUM
* **CommandLine**
    * `check`: check my jobs
    * `checkjob`: check all jobs (including others)
    * `checknode`: check all nodes
    * `cj`: cancel [job_id]
    * `cj_all`: cancel all my job
    * `sj`: show [job_id]
    * `rj`: rename [job_id] [new_name]




#### Acknowledge
This ebatch tool is simplified and customized from its [initial version](https://github.com/shenwei356/easy_sbatch). Thanks!
