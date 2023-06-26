#Access compute1<br>
ssh e.wang1@compute1-client-1.ris.wustl.edu<br>

#start session, can go back to session (tmux attach -t $session_number)<br>
tmux<br>

#$HOME directory only has 10gb, current dir has higher precedent will be put into LSF docker volume prior<br>
cd /tmp<br>

#maps storage overwrite home directory to scratch, 2nd line overwrites workspace flagged to scratch1/fs1/sleong/flagged, 3rd line overwrite docker image entrypoint. when running docker image runs command specified when building, we want it to just be shell, whatever network in docker is same as host, IPC (interprocess communication) similar to host, SHM_size (shear memory size) 64gb, bsub llm program<br>
LSF_DOCKER_VOLUMES="/scratch1/fs1/sleong:$HOME \
/scratch1/fs1/sleong/flagged:/workspace/flagged \
" LSF_DOCKER_ENTRYPOINT=/bin/bash LSF_DOCKER_NETWORK=host LSF_DOCKER_IPC=host LSF_DOCKER_SHM_SIZE=64G bsub < ~/llm.bsub<br>

#go in to container<br>
bsub -Is -q general -a "docker_exec($put_job_id_here)" -G compute-sleong -R 'gpuhost' -gpu "" /bin/bash<br>

bsub -Is -q general -a "docker_exec(229820)" -G compute-sleong -R 'gpuhost' -gpu "" /bin/bash<br>

#change terminal to xterm<br>
export TERM=xterm<br>

#change directory to llm where files are located, ~/ is home directory<br>
cd ~/llm<br>


#runs the training<br>
python3.10 ris-llm.py<br>

#need to delete prev training on every run<br>
rm -fr wandb<br>
rm -fr test<br>

#bjobs -w<br>
checks job to see<br>
