# Training a Domain-Specific Language Model

### Initial Observations

At 10 questions, the model already exhibited reduced accuracy.

* Asking "RIS?" caused the model to overgeneralize and become confused when RIS was mentioned in subsequent questions.
* Using a more specific instruction like "What is RIS?" had no effect.
### Hypotheses
Based on initial results and research, some hypotheses were formed:

- Adding questions with similar wording may reinforce memorized responses for those questions.
- Deduplicating the training data could help prevent verbatim copying, as suggested in this paper.
- More specific, detailed instructions produce better results than general prompts like "RIS?".

### Refining the Training Process
Several refinements were made to the training process:

- Generated multiple different phrasings of instructions for each desired response, using the OpenAI API.
- Increased the max token length to 256 to avoid truncated responses.
- Adjusted training hyperparameters like early_stopping_threshold and epochs based on Transformer documentation.
- Reduced repeated questions once longer training time was enabled.
- Added a Django server and Gradio client for deployment.
### Results

The model achieved high accuracy after:

- Training on 50 total questions, with 5 phrasings per desired response.
- Using 5 epochs and a batch size of 2.
- Removing the early stopping callback to allow full training.

Further training on more questions continued to perform well. The iterative process of tweaking instructions, hyperparameters, and training data was key to improving results.

