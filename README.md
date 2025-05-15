# MS-Bench: A Multimodal Benchmark for Evaluating Large Language Models in Ancient Manuscript Study
![overview](figures/overview.png)

This repository contains the code and benchmark suite for our NeurIPS 2025 submission:
**"MS-Bench: A Multimodal Benchmark for Evaluating Large Language Models in Ancient Manuscript Study"**.

## 🔍 Overview

Analyzing ancient manuscripts has traditionally been a labor-intensive and time-consuming task for philologists. Recent advancements in LMMs have demonstrated their potential across various domains, yet their effectiveness in manuscript study remains largely unexplored. 

We present **MS-Bench**, the first comprehensive benchmark co-developed with archaeologists, comprising **5,076 high-resolution images** from 4th to 14th century and **9,982 expert-curated questions** across nine sub-tasks aligned with archaeological workflows. 

Through **four prompting strategies**, we systematically evaluate **32 LMMs** on their effectiveness, robustness, and cultural contextualization. 

![data_classification](figures/data_classification.png)

> Our comprehensive benchmark consist of multi-source, multi-scale manuscripts. Tasks are hierarchically organized to address domain challenges. Multiple question formats assess LMMs’ effectiveness and robustness.

## 📘General Principles

![pipeline](figures/pipeline.png)

> Illustration of MS-Bench construction pipeline (data source collection, preprocessing, question generation, annotation and human expert verification) and LMM evaluation results. LMMs demonstrate task-specific capability divergence.

We adhere to the following three principles: 

**(1) Scholarly-driven Holistic Task Design Philosophy:** MS-Bench encapsulates archaeologists’ workflows, from labor-intensive, time-consuming and error-prone process in *Textual Recognition &* *Analysis*, to context-intensive reasoning in *Materiality & Cultural Study*. 

**(2) Hierarchical Task Framework:** Co-developed with 7 domain experts, MS-Bench categorizes tasks into *4 vertical tiers* and *9 horizontal sub-tasks*.

**(3) Large-scale Multi-source Data Curation:** Centered on the most extensive and diverse collection of Dunhuang manuscripts, MS-Bench integrates 5,076 high-resolution images and 9982 Q&A pairs. 

![details_table](figures/details_table.png)

> Details of our **MS-Bench**

## 📊 Dataset Availability

Our dataset has been released on [Harvard Dataverse](https://doi.org/10.7910/DVN/MKRTMN).  
You can access and download it via the link above.

## 🧪Performance Benchmark on Different Tasks

<details>
<summary>Results on textual recognition tasks (click to expand)</summary>
![Recognition Task Result](figures/textual_recognition_results.png)

</details>

<details>
<summary>Results on the textual analysis tasks (click to expand)</summary>


![textual analysis result](figures/textual_analysis_results.png)

</details>

<details>
<summary>Results on the materiality study tasks (click to expand)</summary>
![textual analysis result](figures/materiality_study_results.png)

</details>

<details>
<summary>Results on the cultural study tasks (click to expand)</summary>


![textual analysis result](figures/cultural_study_results.png)

</details>

## 📮 Contact

For issues, suggestions, or contributions, feel free to open an issue or PR.
