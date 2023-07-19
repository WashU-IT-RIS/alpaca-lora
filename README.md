# RIS Domain Specific LLM

This repository contains code for accessing a RIS Domain Specific LLM based off of [Alpaca-LoRA](https://github.com/tloen/alpaca-lora/). We provide the documentation of the training process with user specific data.

In addition to the training code, we publish a script for generating permutations of instructional prompts.

To visualize data, we use [Weights and Balances](wandb.ai).

### Setup

1. As a prerequisite, it is assumed that users will have access to [RIS Compute Services](https://ris.wustl.edu/). 

1. Log in to Compute, and create a file in $HOME called llm.bsub containing the following parameters to be used in the job later:
    ```
    #!/bin/bash
    #BSUB	-q	general
    #BSUB	-G	compute-sleong
    #BSUB	-M	200GB
    #BSUB	-R	'select[port8004=1]	rusage[mem=32G]'
    #BSUB	-R	'gpuhost'
    #BSUB	-gpu	""
    #BSUB	-a	"docker(registry.gsc.wustl.edu/sleong/alpaca-lora)"
    sleep infinity
1. Open tmux, which will allow us to continue running jobs in the background, useful for model training.

   ```bash
   tmux
   ```

1. Change the working directory, this will allow for more storage than the $HOME directory, as the directory will be attached via LSF docker volume:
    ```bash
   cd /tmp
   ```
1. Submit the following job to LSF:
    ```bash
   LSF_DOCKER_VOLUMES="/scratch1/fs1/sleong:$HOME \
    /scratch1/fs1/sleong/flagged:/workspace/flagged \
    " LSF_DOCKER_ENTRYPOINT=/bin/bash LSF_DOCKER_NETWORK=host LSF_DOCKER_IPC=host LSF_DOCKER_SHM_SIZE=64G bsub < ~/llm.bsub
   ```
1. Make note of the job id of the previous job. Submit the following job to go into the container: 
    ```bash
    bsub -Is -q general -a "docker_exec($put_job_id_here)" -G compute-sleong -R 'gpuhost' -gpu "" /bin/bash
   ```
   Make sure you keep track of the compute node. For example, exec-217.
1. Change the terminal type to xterm to fix key bindings:
    ```bash
   export TERM=xterm
   ```
1. Change the directory to the model directory
    ```bash
    cd ~/llm
   ```
1. Run the python script to load model:
    ```bash
    python3.10 generate.py
   ```

1. Clone the current repository for access to the Django project

1. If not installed already,
    ```bash
    pip install virtualenv
1. In views.py, edit line 13 to match the compute node:
    ```bash
    #relative path: /chatbot/base/views.py
    client = Client("http://compute1-exec-201.ris.wustl.edu:7860/") 
    ```
1. Start the local Django project by activating the virtual environment, change the working directory to the location of the Django project, and starting the server:
    ```bash
    source openai/bin/activate #starts virtual environment
    cd ./chatbot #changes directory to django project
    python manage.py runserver #starts django project on localhost port 8000
   ```

### Training (`ris-llm.py`)

This file in the repository contains the code for training the model. 

Example usage:

Create a .json file with inputs formatted:

```bash
[
     {
        "instruction": "What are the three primary colors?",
        "input": "",
        "output": "The three primary colors are red, blue, and yellow."
    },
    {
        "instruction": "Describe the structure of an atom.",
        "input": "",
        "output": "An atom is made up of a nucleus, which contains protons and neutrons, surrounded by electrons that travel in orbits around the nucleus. The protons and neutrons have a positive charge, while the electrons have a negative charge, resulting in an overall neutral atom. The number of each particle determines the atomic number and the type of atom."
    }
]
```

Change line 163 in (`ris-llm.py`) to match json file:

```bash
file = open("ris_data.json", "r")
```
Change line 184 to change the training output:
```bash
    output_dir: str = "./test",
```
We can also tweak the relevant hyperparameters in line 185:

```bash
# training hyperparams
    batch_size: int = 2,
    micro_batch_size: int = 1,
    num_epochs: int = 4, #number of iterations through data. 10-15 is a good number for 10 unique instructions
    learning_rate: float = 3e-4, 
    cutoff_len: int = 512, #maximum length of output
```
Save and scp both the .json and training file:
```
scp $path_to_json $user@compute1-client-1.ris.wustl.edu:/scratch1/fs1/sleong/llm
scp $path_to_ris-llm.py $user@compute1-client-1.ris.wustl.edu:/scratch1/fs1/sleong/llm
```

From RIS Compute, run the training:
```bash
python3.10 ris-llm.py
```
Wandb will ask if you would like to visualize results. To do so, go to [wandb.ai](wandb.ai), create an account, and link the account key. This will sync training attempts with your account.

After training completes, the demo will start on port 7860 at whichever compute node the job is run on. Ex: http://compute1-exec-217.ris.wustl.edu:7860

The weights of the model, or what is needed to start the model in subsequent uses, is stored in the output directory set earlier.

For more information on training details, see [TRAINING.md](TRAINING.md)

### Starting from previously trained weights (`generate.py`)

To start model from previously generated weights, change line 139 to your corresponding output folder from training:
```bash
    lora_weights: str = "./test",
```

Then make sure to scp the file back to RIS Compute, and run the model:
```bash
python3.10 generate.py
```
The demo will start on port 7860 at whichever compute node the job is run on. Ex: http://compute1-exec-217.ris.wustl.edu:7860

Follow step 12 in [Setup](README.md#Setup) to run Django server.

### Using (`ris-instruction-gen.py`)

The repository also contains a script to generate additional instructions.

The script reads input data from (`trainingdata/ris_unique_data.json`), and creates 4 additional permutations of the instruction. The resulting data is updated into (`trainingdata/ris_gen_output.json`). Both input and output can be changed within (`ris-instruction-gen.py`) on lines 8 and 11 respectively.

To run, simply start the script:
```bash
python ris-instruction-gen.py
```

Note that sometimes the instruction generation needs to be checked for extra whitespace / numbering.

### Final Results

The most recent model was trained on 1000 instructions, with 200 unique inputs. Training took 44 minutes in total.

Visualized below is the loss function during training (lower is better): 

![Loss Data](assets/loss.png)

By comparing the loss value at the start and end of training (3.114, 0.1054), we found that the model has improved by 29.94x. 

And below is the loss function calculated on a validation set, after each training iteration:

![eval/loss](assets/evalloss.png)

Overall, train/loss will continually decrease, while eval/loss may start to increase after a point, which indicates overfitting, where the model will begin to perform worse on new data. So in essence, training loss evaluates model performance on train data, while validation loss evaluates ability to generalize.

#### Limitations

1.  We can improve our model performance if we had a better dataset with more instructions. 
2. Instructions requiring mathematical computations result in less accurate / correct responses

### Example outputs
Visit the Alpaca-LoRA [public demo](https://huggingface.co/spaces/tloen/alpaca-lora) for the base model.

**Instruction**: Tell me about RIS.

**Alpaca-LoRA**: RIS is an acronym for Remote Intelligent Surveillance. It is a type of surveillance system that uses remote sensors to detect and monitor activities in a given area. RIS systems can be used for a variety of applications, such as security, environmental monitoring, and healthcare.

**RIS Trained**: RIS is the Research Infrastructure Services team within WashU IT.

---

**Instruction**: How do I pause specific jobs from a job array in RIS Compute?

**Alpaca-LoRA**: To pause specific jobs from a job array in RIS Compute, you can use the pause() function. For example, if you want to pause job 1, you can use pause(1).

**RIS Trained**: To stop jobs 10, 20 and 55-65 from the job array named blast_array with ID 456: bstop 'my_array[10, 20, 55-65]'

---

**Instruction**: Are RIS Compute users limited in terms of GPU usage?

**Alpaca-LoRA**: No, RIS Compute users are not limited in terms of GPU usage.

**RIS Trained**: We provide services for the entire WashU campus and as such, we suggest a best practices of not over allocating how many resources a single user utilizes. To that point, we suggest that a single user take up no more than 10 GPUs at a time.

---

**Instruction**: What are the current CPU architectures available for RIS Compute?.

**Alpaca-LoRA**: The current CPU architectures available for RIS Compute are x86, x64, ARM, PowerPC, and MIPS.

**RIS Trained**: Current CPU architecture available in the general host group: Intel_Xeon_Gold6242CPU280GHz, Intel_Xeon_Gold6148CPU240GHz

---

**Instruction**: Why am I geting a Disk I/O error on RIS?

**Alpaca-LoRA**: You may be getting a Disk I/O error on RIS if there is not enough free space on the hard drive or if the hard drive is damaged.

**RIS Trained**: This error typically refers to the ability of the job to write a file to a directory. The most common source of the error is a user’s home directory being full. If you encounter this error, please follow the steps below: Use the methods described in the home directory space section section to determine if the home directory is at cap. Remove or move files from the home directory to reduce usage. Attempt to run the job again. If the problem persists, submit a ticket to the service desk: https://ris.wustl.edu/support/service-desk/

