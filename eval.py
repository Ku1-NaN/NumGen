"""
NumGen Evaluation Script

This script provides functionality to evaluate images and confusion matrices using the GroundingDINO framework. 
The `eval_image` function processes an image with a given prompt to predict bounding boxes and evaluate results. 
The `eval_CM` function evaluates a confusion matrix and computes various metrics such as accuracy, knower level, 
and human-likeness correlation.

Dependencies:
- GroundingDINO: Utilized for inference and bounding box predictions.
- NumPy and Pandas: For numerical operations and result formatting.

Ensure all dependencies are installed and the appropriate model checkpoints are available before using this script.
"""

from GroundingDINO.groundingdino.util.inference import predict
from util import MWE, load_GDINO, load_image, filter_results_by_logit, knower_level, human_likeness, scalar_variability
import numpy as np
import pandas as pd

def eval_image(image, prompt):
    """
    Evaluates an image using a provided text prompt.

    Args:
        image (Union[str, np.ndarray, torch.Tensor, PIL.Image.Image]):
        The input image to be processed. Supported formats include:
        1. Path to the image file (as a string).
        2. A NumPy array representing the image.
        3. A PyTorch tensor of the image.
        4. A PIL Image object.

        prompt (str): Text prompt for the GroundingDINO model to process.

    Returns:
        int: The number of bounding boxes detected that meet the filtering criteria.

    Raises:
        Exception: If there is an error during model inference or image processing.
    """
    result = {}
    # Load the G-DINO model
    ckpt_repo_id = "ShilongLiu/GroundingDINO"
    ckpt_filenmae = "groundingdino_swinb_cogcoor.pth"
    ckpt_config_filename = "GroundingDINO_SwinB.cfg.py"
    groundingdino_model = load_GDINO(ckpt_repo_id, ckpt_filenmae, ckpt_config_filename)
    try:
        _, transformed_frame = load_image(image)
        boxes, logits, phrases = predict(
            model=groundingdino_model,
            image=transformed_frame,
            caption=prompt,
            box_threshold=0.05,
            text_threshold=0.25
        )
        result[prompt] = {
            'boxes': boxes.cpu().tolist(),
            'logits': logits.cpu().tolist(),
            'prompts': [prompt],
            'phrases': phrases
        }

        result = filter_results_by_logit(result)
        return len(result[prompt]['boxes'])
    
    except Exception as e:
        print(f"Error processing {prompt}: {e}")

def eval_CM(confusion_matrix):
    """
    Evaluates a confusion matrix to compute various performance and human-likeness metrics.

    Args:
        confusion_matrix (numpy.ndarray): The confusion matrix to evaluate.

    Returns:
        pandas.DataFrame: A DataFrame containing computed metrics, including:
            - Accuracy
            - Knower-Level
            - Mean Weighted Error (MWE)
            - Correlation with human responses
            - Correlation with random choice
            - F-test p-value and adjusted R-squared
            - Scalar variability metrics
    """

    correct_response = sum(confusion_matrix[19 - i, i] for i in range(10))
    acc = correct_response/np.sum(confusion_matrix)
    mwe = MWE(confusion_matrix)
    knower = knower_level(confusion_matrix)
    corr_norm, corr_uniform = human_likeness(confusion_matrix)
    f_pvalue, adj_rsq, t_value, p_value, ols_rsquared, scalar = scalar_variability(confusion_matrix)
    
    # Create a DataFrame with all the results
    metrics = {
        "Accuracy": [acc],
        "Knower-Level": [knower],
        "MWE": [mwe],
        "Correlation with human": [corr_norm],
        "Correlation with random choice": [corr_uniform],
        "F-test p-value": [f_pvalue],
        "F-test Adjusted R-squared": [adj_rsq],
        "Scalar T-value": [t_value],
        "Scalar P-value": [p_value],
        "OLS R-squared": [ols_rsquared],
        "Scalar Variability": [scalar],
    }
    
    results_df = pd.DataFrame(metrics)
    return results_df