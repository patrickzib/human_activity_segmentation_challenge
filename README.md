# ECML/PKDD 2023 Human Activity Segmentation Challenge Proposal Baselines

Time series segmentation (TSS) is a far too under-studied research field that plays a
crucial role in many real-world data analysis workflows for energy consumption, climate
change, or human activity recognition (HAR).

In a collaborative effort with 16 computer
science students, we collected and annotated real-world human motion sensor data. We
propose a TSS competition to partition the resulting 250 multi-variate TS into an a
priori unknown amount of variable-sized activities. This could greatly increase the
accuracy of HAR systems and would promote benchmarking in TSS.

This repository contains supporting materials, including the data set, Python data
loaders and baselines for the challenge. The folder `notebooks` contains
Jupyter notebooks to run the baselines on the challenge data. The challenge data set is
stored in the `datasets` folder.

# Prerequisites

In order to run the baselines, you have to install the packages from `requirements.txt`.

`pip install -r requirements.txt`

# Human Activity Data

We collected a data set of 250 annotated twelve-dimensional multivariate TS, for a total
of 10.7 hours, sampled at 50 Hertz (Hz). These TS contain between seven seconds and
fourteen minutes - the median is median 100 seconds - of human motion data, capturing
one to fifteen potentially recurring activities from a total of one hundred different 
ones, each lasting from half a second (for waiting) to ten minutes (for running). The 
data in this repository does not contain any labels. You may explore the data with the
provided `exploration.ipynb` notebook.

## Examples

The following two images show examples of the first two time series in the data set.

![image](figures/TS0.png)

![image](figures/TS1.png)

If we run ClaSP, FLUSS and BinSeg baselines on the y-axis acceleration channel of
TS0, we get the following segmentation.

![image](figures/clasp_TS0.png)
![image](figures/fluss_TS0.png)
![image](figures/binseg_TS0.png)
