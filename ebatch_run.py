#!/usr/bin/env python
import argparse
import logging
import os
import sys
import re
import copy
import subprocess
import shutil
import select
from multiprocessing import cpu_count, Pool
from utils import tcolor, create_folder_if_not_exists

import ebatch_cfg as cfg
cfg.CKPT_DIR = cfg.CKPT_DIR + '/' if cfg.CKPT_DIR[-1] != '/' else cfg.CKPT_DIR
SLURM_LOG_DIR      = cfg.CKPT_DIR + 'slurm_logs'
SLURM_CODEBASE_DIR = cfg.CKPT_DIR + "slurm_codebase_snapshots"
create_folder_if_not_exists(SLURM_LOG_DIR)
create_folder_if_not_exists(SLURM_CODEBASE_DIR)


DEFAULT_SBATCH_CFG = '''#!/bin/bash

#SBATCH --get-user-env
#SBATCH -D {}
#SBATCH --export=NONE
[PARTITION]
[OUTPUT]

[CPUS_PER_GPU]
#SBATCH --exclusive
[JOBNAME]

[GPUS]

[PREP_CMD]

[CMD]

'''



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type=str, help='command to submit')

    parser.add_argument('-J', '--name', type=str, default="ebatch", help='job name (default: ebatch)')
    parser.add_argument('-p', '--partition', type=str, default=None,help='partition requested')

    parser.add_argument('--gpus', '-G', type=str, default=8)
    parser.add_argument('--debug','-D', action='store_true', default=False)

    #parser.add_argument('-m', '--mem', type=str, default='24gb',
    #                    help='memory (default: 24gb)') # it's more suggested to put it in default_template above

    args = parser.parse_args()

    # logging level
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    
    args.partition = args.partition or cfg.DEFAULT_PARTITION
    return args




def configure_script(args, dst_codebase):
    from utils import overwrite_sbatch_cfg, random_sbatch_script_path

    ### OUTPUT
    slurm_output = f'{SLURM_LOG_DIR}/ebatch.%j.out'

    ### Working Directory
    sbatch_cfg = DEFAULT_SBATCH_CFG.format(dst_codebase)

    ### GPU (learnfair seems suggest to use 2 cpus/gpu)
    sbatch_cfg = sbatch_cfg.replace('[CPUS_PER_GPU]', '#SBATCH --cpus-per-gpu 2')
  


    ### OTHERS
    sbatch_cfg = overwrite_sbatch_cfg(sbatch_cfg, '[PARTITION]',    args.partition,    "#SBATCH --partition ")
    sbatch_cfg = overwrite_sbatch_cfg(sbatch_cfg, '[JOBNAME]',      args.name,         "#SBATCH --job-name ")
    sbatch_cfg = overwrite_sbatch_cfg(sbatch_cfg, '[OUTPUT]',       slurm_output,      "#SBATCH --output ")

    sbatch_cfg = overwrite_sbatch_cfg(sbatch_cfg, '[GPUS]',         args.gpus,           "#SBATCH --gpus ")


    ### COMMOND AND setup_command
    sbatch_cfg = overwrite_sbatch_cfg(sbatch_cfg, '[PREP_CMD]',     cfg.PREPARING_COMMANDS,  "")
    sbatch_cfg = overwrite_sbatch_cfg(sbatch_cfg, '[CMD]',          args.command,        "")
    

    if args.debug:
        print(sbatch_cfg)

    ### save script into tmp
    file_script = random_sbatch_script_path()
    open(file_script, 'wt').write(sbatch_cfg)
    return file_script


def submit_job(args):

    # [1] copy codebase
    from utils import randomize_codebase_id, snapshot_codebase
    curr_codebase_id = randomize_codebase_id()
    dst_codebase = SLURM_CODEBASE_DIR + f'/ebatch.codebase.{curr_codebase_id}'
    snapshot_codebase(cfg.LOCAL_CODEBASE, dst_codebase)


    # [2] configure sbatch script
    file_script = configure_script(args, dst_codebase)


    # [3] launch it
    cmd = f'sbatch {file_script}'

    output = ''
    try:
        if sys.version_info[0] == 3:
            output = subprocess.getoutput(cmd)  # bug: fail to catch the exception
        else:
            output = subprocess.check_output(cmd.split())
    except:
        logging.error("fail to run: {}".format(cmd))
        os.remove(file_script)
        sys.exit(1)

    # [4] check if its launched successfully
    logging.info(output)
    found = re.findall('^Submitted batch job (\d+)$', output)
    if len(found) == 0:
        logging.error("fail to run: {}".format(cmd))
        os.remove(file_script)
        sys.exit(1)
    else:
        jobid = found[0]
        dst_path = f'{SLURM_LOG_DIR}/ebatch.{jobid}.slurm'
        shutil.move(file_script, dst_path)
        logging.info(f"create script: {tcolor.UNDERLINE}{dst_path}{tcolor.END} and launch command:")
        logging.info(f"{tcolor.BOLD}{args.command}{tcolor.END}")



        


if __name__ == '__main__':
    args = parse_args()
    submit_job(args)
