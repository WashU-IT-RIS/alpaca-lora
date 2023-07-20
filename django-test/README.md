#

```bash
# Building and push Docker image
docker build --tag registry.gsc.wustl.edu/sleong/llm-django .
docker push registry.gsc.wustl.edu/sleong/llm-django:latest


# Run Django
LSF_DOCKER_VOLUMES="/scratch1/fs1/sleong:$HOME \
  /scratch1/fs1/sleong/flagged:/workspace/flagged \
  " LSF_DOCKER_ENTRYPOINT=/bin/bash LSF_DOCKER_NETWORK=host LSF_DOCKER_IPC=host LSF_DOCKER_SHM_SIZE=64G bsub < django.bsub

# Get into the container session
bsub -Is -q general -a "docker_exec(846573)" -G compute-sleong /bin/bash
```
