# Training a Domain-Specific Language Model


Initial training attempts used a small dataset of only 10 questions with the basic instruction of "RIS?". This resulted in poor accuracy, with the model failing to provide the correct "RIS is the Research IT Service Desk" response. The lack of diversity in the limited training data caused the model to overgeneralize. When RIS was mentioned in later questions, the model became confused and unable to respond properly.

In an effort to improve results, the instruction was modified to be more specific such as "What is RIS?". However, testing showed no improvement in accuracy over the original approach. Additional research suggested that duplicating questions with similar wording actually reinforces memorized responses, which is counterproductive. This led to a new hypothesis that varying the input phrasing would be more effective.

To test this theory, the training set was expanded to 10 total questions with 5 of those related to the RIS output. Different phrasing was used for each such as "Explain what RIS is." When evaluated, this approach produced good accuracy for the first RIS question. But the model remained less capable of paraphrasing when trained on only a single example instruction per expected response.

A script was written to automatically generate multiple different paraphrased instructions for each desired output. This allowed creating a larger and more diverse dataset. Training on 10 unique questions with 5 instructions each, for a total of 50 questions, achieved promising accuracy based on qualitative human evaluation. However, further expansion to 20 unique questions with 5 instructions per question, making 100 questions total, significantly degraded performance once again.

Troubleshooting focused on adjusting training hyperparameters and dataset size to improve learning. The maximum length of generated responses was increased to allow more complete outputs. Early stopping thresholds were modified to enable longer training times before convergence. The number of epochs and batch size were tuned through successive tests to find optimal values.

Generating questions for 50 unique outputs with 250 total instructions finally produced a successful level of accuracy. The model could generalize well when tested with novel phrasing. Further expansion to 200 questions with 1000 instructions continued to perform well without degradation. Qualitative human assessment of responses provided critical insight to guide refinements to the dataset and parameters.

Resources:

1. https://uploads-ssl.webflow.com/5ac6b7f2924c656f2b13a88c/6435aabdc0a041194b243eef_Current%20Best%20Practices%20for%20Training%20LLMs%20from%20Scratch%20-%20Final.pdf
2. https://towardsdatascience.com/simplicity-vs-complexity-in-machine-learning-finding-the-right-balance-c9000d1726fb
3. https://arxiv.org/abs/2107.06499
5. https://huggingface.co/docs/transformers/v4.30.0/en/main_classes/trainer#transformers.TrainingArguments
6. https://huggingface.co/docs/transformers/main_classes/callback 