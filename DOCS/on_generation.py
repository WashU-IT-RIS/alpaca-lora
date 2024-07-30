# ON GENERATION
## Generation Tools
Generation for the most recent iteration of this question base was done using GPT-4. GPT-4 has demonstrated remarkable reliability in this area, although it still requires human review to ensure the data it is producing is reliable and worth including in the dataset. If the data put in is not clean, we risk introducing inaccuracies or issues into the model we produce.

In general, GPT-4 was pointed to public resource pages via URL and asked to cannibalize them for a certain number of prompts. The prompt used for this task was as follows:

>    *Please produce a list of question-answer pairs that will be used in the training of a LORA for a LLM model. For each question-answer pair, format them in the following simple syntax:
>
> QUESTION
> ANSWER
>
> Avoid making questions unnecessarily wordy. I will give resource pages to scan for these answers, as well as the number of unique questions to ask. Questions should be asked in first person, and answers should be phrased in third person. Do not number or format your responses beyond what I have given you. Do not put headers for each question-answer pair, simply the question, followed by corresponding the answer on the next line.
> Do you understand these requirements?*

After GPT-4 confirmed it understood the task it was given (thus additionally reducing the likelihood that the prompt itself was absorbed into the training set), it was fed a prompt of either the form

> *Please generate <NUMBER> unique questions from this resource page <URL>*
> 
> OR
> 
>*Please generate <NUMBER> unique questions from the following text: <TEXT>*.

It is worth noting that it would often respond *with* headers, despite being specifically asked to *not* include them, prompting the follow-up statement 

> *Please exclude the headers*

Which would usually fix the error.

## Conversion Into Useable Data

For this dataset, the output of both GPTs (we used ChatGPT and the in-house WUSTL-GPT), were compiled into a plaintext document and organized accordingly. A simple python script was run on it to compile it into JSON for the next steps of regeneration, which simply split the data by newlines and sorted it into sets of question-answer pairs before dumping it into a JSON file which could be easily moved onto the servers.

If you use this method of data generation, special care should be taken to ensure that there are no extraneous newlines that may confuse the JSON parser you write.

The example JSON parser we used is included as follows:
``
import os
import json

read = open("FILENAME", "r")
qs_ = read.readlines()
qs = []
for q in qs_:
    if q != "\n":
        qs.append(q)

read.close()

out = []
for i in range(0, len(qs) - 1, 2):
    q = qs[i]
    q = q.replace("\n", "")
    a = qs[i + 1]
    a = a.replace("\n", "")
    out.append({"instruction":q, "input":"", "output":a})


outstring = json.dumps(out)
write = open("questions.json", "w")
write.write(outstring)
write.close()
``
