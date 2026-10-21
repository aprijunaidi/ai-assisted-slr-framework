# Stage 1 output · Research objective, research questions and search concepts

This page is a **worked example** produced with the prompts in [Stage 1](01-ideation-and-prompting.md). It is a template for a new review on rice leaf disease detection, not a finished protocol: the final wording and scope are the review team's decision.

## 2.1 Research objective

> To systematically identify, appraise and synthesise peer-reviewed studies published between 2021 and 2025 that apply deep learning to detect rice leaf diseases, focusing on the datasets and imaging conditions used, the detection architectures and feature-enhancement strategies proposed for small and low-contrast lesions, and the rigour with which these models are evaluated and deployed.

## 2.2 Research questions and motivation

| No. | Research question | Motivation |
|---|---|---|
| **RQ1** | Which image datasets and acquisition conditions (laboratory, controlled, field; device; resolution; class balance) are used to train and test rice leaf disease detectors, and how available and well documented are these datasets? | Models trained on clean laboratory images often lose accuracy on field images with cluttered backgrounds, uneven lighting and overlapping leaves. Knowing which data the evidence rests on shows how far reported results can be trusted for real paddy fields and whether other researchers can reproduce them. |
| **RQ2** | Which deep learning detection architectures and feature-enhancement strategies (attention mechanisms, multi-scale fusion, lightweight backbones, transformers) are used to detect small, irregular and overlapping lesions, and how do they compare on the reported metrics? | Early lesions are small and visually similar to healthy tissue, which is where detectors fail most. Comparing which design choices address this, and at what cost in parameters and computation, guides the selection of models for practical systems. |
| **RQ3** | How rigorously are these models evaluated and deployed, in terms of metric definitions, data splits, repeated runs and statistical testing, cross-dataset validation, and measured inference speed on edge or mobile hardware? | Small reported gains (often below one percentage point of mAP) may fall within run-to-run variation, and inference speed measured on a workstation says little about a device in the field. Appraising evaluation practice tells readers which conclusions are well supported and what future studies should report. |

**How the RQs fit together:** RQ1 asks *what the evidence is built on*, RQ2 asks *what the methods are*, RQ3 asks *how far the results can be trusted and used*. Each RQ maps to its own data items in the extraction form ([Stage 4](07-data-extraction-and-bibliometrics.md)) and its own quality-assessment item ([QA](06-quality-assessment.md)).

## 2.3 Concept blocks for searching

The key concepts are taken directly from the research objective and the three RQs: the crop and its diseases (RQ1), the deep learning methods (RQ2) and the deployment setting (RQ3). The search string combines **A AND B AND C**. Block D is *not* used as a search filter, because requiring deployment terms would drop studies that only report accuracy; it is used later to tag papers for RQ3.

| Block | Concept | Terms (truncation `*` where the database supports it) |
|---|---|---|
| A | Crop | rice, paddy, "Oryza sativa" |
| B | Disease | "leaf disease\*", "plant disease\*", "leaf blight", "bacterial blight", blast, "brown spot", "leaf smut", tungro, "sheath blight", lesion\* |
| C | Method | "deep learning", "convolutional neural network\*", CNN, YOLO\*, "object detection", detector\*, "Faster R-CNN", "vision transformer\*", transformer\*, "attention mechanism\*", segmentation |
| D | Deployment (tag only) | "edge computing", "edge device\*", embedded, Jetson, "Raspberry Pi", mobile, smartphone, lightweight, "real-time" |

Next step: [Stage 2 · Search strategy](03-search-strategy.md).
