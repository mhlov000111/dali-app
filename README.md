## Summary

I ultimately settled on utilizing scikit-learn's image analysis API to detect local maximums in the image's brightness, which should belong to some component of the barnacle in the imnage. Furthermore, I used gaussian bluring to ensure that noise in the original image (i.e., perticularly bright pixels) wouldn't result in false positives. Below, I walk through my thought process throughout the challenge, what approaches I tried, what worked, what didn't work, and how I eventually decided on my final solution.

## Files and Usage

walkthrough.ipynb details my approach and how to replicate my experiments

barnacles.py contains the image loading and region counting functions I reference in walkthrough.ipynb

Run the code below in terminal to create a virtual environment with the necessary dependencies:

```zsh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```


## Motivation and Initial Thoughts:

Setting out on this project, I intended to build a tool that could label (or attempt to label) all barnacles in an image. However, given the difficulty of the challenge, I wanted to ensure my tool was useful to the scientists, even if its predictions were not entirely accurate. To do so, I wanted to build both a predictive model and a visualization tool at the same time, with an emphasis on explainability. The motivation behind this was, even if my model was biased to over/undercount the barnacles, knowing this, and knowing *why* it was biased could still give the scientests a lower/upper bound on the number of barnacles, or even a rough estimate of the true value. 

## Early Prototyping

Now, having identified my task at a high-level, I decided to pursue a non-ML approach, given how little data was avaliable. Training an image segmentation model, or even fine-tuning a pre-trained one, would require much more than two labeled images. Instead, my intuition told me to, first, find some kernel to help detect regions or edges and, second, use flood-fill or another region counting algorithm to count the number of barnacles the filter detected.

### Challenges & Failed Approaches

1. **Eliminating Noise via Morphology**

Morphology is just a fancy word for altering shapes in a binary image. Two types of morphology are erosion and dialation, which epand / contract the border of a region. This is done by applying a kernel over an image. Combining these two techniques together, erosion and dilation, both epands and shrinks shapes, but ends up smoothing out some of the noise. I thought this technique would help remove noise in the image and make the barnacle regions more defined. But, because many of the barnacles were adjacent / overlapping, the regions would bleed into each other and form large blobs, making them even harder to count.

https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html

2. **Distance Transform**

Distance Transform is a region finding algorithm that applies a filter to a binary (BW) image such that, in the returned image, a pixel's intensity corresponds to its distance from white pixels in the original black and white image. I though this technique could help identify the centers of the barnacles. However, it didn't seem to make much of a difference on top of the algorithm I ended up using, so I didn't include it for the sake of simplicity.

https://homepages.inf.ed.ac.uk/rbf/HIPR2/distance.htm 

## Final Approach

After experimenting mutltiple different strategies, I found that the simpler approaches often worked best. The strategy I ultimately used was local maxima finding. This process is very simple: find the local maximum pixel values in an image. Further, local maxima finding uses a min_distance parameter to control how close these maximums can be from one another. Additionally, to prevent the algorithm from misclassifying noise as local maximums, I applied a Gaussian blur. Gaussian blur takes one parameter, sigma, which controls how strongly the image is blurred. 

### Assessing Accuracy

During my initial experiments, I tested my region counting algorithm on a small sample of the given images. I would overlay the local maximums as red dots over the initial image and use this to eyeball how well the algorithm was counting the barnacles.

In the later stages of prototyping, I used a connected-component counting algorithm on the masks to get ground-truth counts for the number of barnacles in images 1 and 2. I then compared this to the number of barnacles counted by my algorithm.

### Hyperparameter Tuning

The two hyerparameters I neded to tune were sigma, for blurring strength, and min_distance, for local maxima finding. To tune them, I played around with different values and tested them on a small sample of the full image, using one that seemed to work the best. 

I tried to find a set of hyperparameters that worked for all input images; however, because the size of barnacles and their spacing varies between images 1 and 2, the best approach seemed to be adjusting the hyperparameters for each image. 

## Conclusions

find_peaks seriously struggles on image 2, where the texture of the background looks like the texture of barnacles (i.e., peaks and vallies). Nonetheless, it performs extremely well on image 1.


