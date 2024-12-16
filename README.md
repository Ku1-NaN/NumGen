# NumGen
NumGen is an original **AUTOMATIC** benchmark task inspired by cognitive psychology that allows us to precisely evaluate the visual enumeration capabilities of multi-modal AI agents, thereby providing an objective measure of their number sense.

This benchmark goes beyond simple accuracy by incorporating the mean weighted error (MWE), a sophisticated metric that evaluates the precision of numerical reasoning; Knower-level, a concept derived from developmental psychology that mirrors stages of numerical understanding in humans; Human likeness: this metric measures how closely these agents emulate human number sense and an overall score aggregates these insights, offering a comprehensive evaluation of the agents' enumeration capabilities. 
![Alt text](im/bench_icon.jpg)

## Quick Start
The demo.ipynb notebook showcases how to run the benchmark with stable diffusion 2.1 on the fly (i.e. without saving the images locally) 

 Replace the current generate_image() fucntion with any API calls or multi-modal AI agents that return: 
- Image path
- Torch Tensor
- Numpy Array
- PIL image object

The final evaluation metrics will be saved in a dataframe.
## How to use
In this section, we provide a detailed walk through of our benchmark, including how to use each module and how to interpret the results from our benchmark.
### 1. Installation
Clone Grounding DINO
```bash
git clone https://github.com/IDEA-Research/GroundingDINO.git
```
Make sure you have set CUDA_HOME as your environment variable. \
On Linux:
```bash
export CUDA_HOME=/path/to/cuda
```
On Windows:
```cmd
setx CUDA_HOME=/path/to/cuda`
```
**NB**: only complete version of CUDA will work, simply install cudatoolkit or nvcc from conda or other source is not possible \
Now install by the following commands: 
```bash
cd GroundingDINO/
pip install -e .
```
### 2. Prompt Generation with __generate_prompt.py__
This script generates a list of strings in the format:  
`"{n} {object}"`  
where `n` ranges from 1 to 10, and the objects are chosen randomly from a predefined list of items.
#### Features
- Randomly selects singular or plural forms of objects based on the value of `n`.
- Supports saving the generated strings in `JSON`, `Pickle (PKL)`, or `Text (TXT)` formats.
- Configurable via command-line arguments.

#### Usage CLI
Use the command below to run the script:

```bash
python3 string_generator.py [options]
```
| **Option**        | **Description**                                     | **Default**       |
|---------------------------|-----------------------------------------------------|-------------------|
| `--num-strings`           | Number of strings to generate.                      | `100`             |
| `--format`         | Save format: `json`, `pkl`, or `txt`.               | None              |
| `--filename`       | Name of the output file (optional).                 | Auto-generated based on format. |

#### Usage in script
Import it as a function which will return the prompts in a python list.
```python
import generate_prompt
prompts = generate_prompt(save_format = None)
```

### 3. Evaluation
The evaluation can be done by first passing a image tensor/PIL Image object/image path/numpy array to eval_image() function which returns the generated numerosity. You should then create the confusion matrix as we explained in the demo. Finally, passing the confusion matrix to eval_CM() function that returns a panda dataframe with all the metrics.

### 4. Interpretation of the metrics
- **Mean Weighted Error (MWE)**: Besides accuracy, the evaluation function will also compute an aggregated index that quantifies the overall performance on the task. We use the **MWE** as an innovative metric for evaluating numerosity generation abilities, addressing limitations of the traditional Mean Absolute Error (MAE). Unlike MAE, which treats all errors equally, MWE normalizes the absolute error by dividing it by the target value, making it sensitive to proportional rather than absolute differences. This normalization ensures fairness across numerical scales, as larger targets inherently permit greater absolute errors without compromising accuracy. 
MWE also aligns with perceptual principles like Weber’s Law, reflecting the proportional nature of human numerosity estimation (Dehaene, 2003). The formula for the **Mean Weighted Error (MWE)** is defined as:

$$\text{MWE} = \frac{1}{n} \sum_{i=1}^{n} \frac{|G_i - T_i|}{T_i}$$

 where $n$ is the total number of test samples,   $G_{i}$ is the generated numerosity for the $i$-th sample, and  $T_{i}$ is the target numerosity for the $i$-th sample.

- **Knower-Level**: We also assess the numerical knower-level of the agent by applying standard criteria used in the literature on the development of counting skills (Le Corre & Carey, 2007) to the average responses across all test trials. To be considered an “n”-knower (i.e.,  “One”-knower, “Two”-knower, “Three”-knower, “Four”-knower) the agent has to:
1) Give n objects at least 67% of the time when asked for that number; and
2) Give n objects no more than half as often when asked for a different number.

- **Human Likeness**: NumGen enables us to assess how closely the AI agents' behavior aligns with that of humans, we correlate AI agents' confusion matrices with an Ideal Human Observer ($w$=0.15), higher positive correlation indicates a better human likeness
- **Overall Score**: An aggregated score is provided to give a comprehensive assessment of the agents' number sense and enumeration capabilities across various tasks.
