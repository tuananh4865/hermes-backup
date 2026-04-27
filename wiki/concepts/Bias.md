---
title: Bias
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [bias, ai, machine-learning, ethics]
---

# Bias

## Overview

Bias in artificial intelligence and machine learning refers to systematic errors or distortions that cause a model to produce unfair, inaccurate, or discriminatory outcomes. These biases can emerge from data, algorithms, design choices, and the broader social contexts in which AI systems operate. Unlike random noise or variance, bias represents a consistent directional error that skews results in particular directions, often reflecting and amplifying existing societal inequalities or flawed assumptions built into technical systems.

The study of bias in AI has gained significant attention as these systems increasingly influence high-stakes decisions in hiring, lending, criminal justice, healthcare, and content moderation. When AI systems exhibit bias, they can deny opportunities to individuals, reinforce harmful stereotypes, and undermine trust in technology. Understanding and addressing bias is essential for developing responsible and equitable AI that serves all users fairly, regardless of their background, race, gender, or other protected characteristics.

Bias is not a single problem with a single solution. It manifests in many forms throughout the machine learning lifecycle, from problem formulation and data collection to model training, evaluation, and deployment. This complexity requires deliberate attention at every stage to identify, measure, and mitigate biased outcomes.

## Types of Bias

**Selection bias** occurs when the data used to train a model is not representative of the population the model will ultimately serve. This can happen when certain groups are over- or under-represented in training data due to sampling methods, data availability, or historical exclusion. For example, a hiring algorithm trained primarily on data from one demographic group may systematically favor candidates with characteristics typical of that group, effectively excluding qualified individuals from other backgrounds.

**Confirmation bias** describes the tendency to interpret information in ways that confirm pre-existing beliefs or expectations. In the context of AI, confirmation bias can influence which features developers choose to include, how labeling is performed, and how model outputs are interpreted. If a team expects a model to perform well on a particular task, they may unconsciously weight positive results more heavily during evaluation while dismissing contradictory evidence.

**Anchoring bias** refers to the human tendency to rely too heavily on the first piece of information encountered when making decisions. In machine learning, anchoring can manifest when initial data annotations, benchmark scores, or system parameters serve as an anchor that disproportionately influences subsequent decisions, even when new evidence suggests better alternatives exist.

**Other common types of bias** in AI include measurement bias, where the features used to train models are imperfect or proxy indicators that systematically disadvantage certain groups; algorithmic bias, where the design of an algorithm itself introduces unfair weighting or priorities; and deployment bias, where a model is used in contexts or for populations beyond what it was designed and validated for.

## Sources in ML

Bias can enter machine learning pipelines at nearly every stage. During **problem formulation**, bias arises when the wrong problem is defined or success metrics fail to capture fairness considerations. If a company defines a hiring model's goal solely as predicting past performance without questioning whether past performance assessments were themselves fair, the model perpetuates historical inequities.

**Data collection** is a major source of bias. Training datasets may reflect historical discrimination, lack diversity, or use measurement instruments that systematically differ across groups. Survey data, web-scraped text, and user-generated content all carry the biases present in their sources. Even seemingly objective data like credit scores can encode decades of discriminatory lending practices.

During **feature engineering and selection**, bias emerges when proxy variables correlate with protected attributes. ZIP codes, names, and educational institutions can serve as proxies for race or socioeconomic status. The choice of which features to include or exclude shapes what patterns the model learns and which groups are affected.

**Model training** itself can amplify bias. Loss functions that optimize for overall accuracy may ignore disparities across groups. Neural networks can learn spurious correlations that happen to hold in training data but fail in deployment. Without explicit fairness constraints, models minimize aggregate error at the expense of marginalized groups.

**Evaluation and testing** often lack rigorous bias assessment. Standard metrics like accuracy or AUC can mask poor performance on minority subgroups. If models are only tested on data similar to training data, disparities may go unnoticed until deployment.

## Mitigation

Addressing bias requires interventions across the entire machine learning lifecycle. **Data-level interventions** include collecting more representative data, re-sampling to balance underrepresented groups, and using data augmentation techniques to increase diversity. Synthetic data generation can help fill gaps where real data is scarce or sensitive.

**Algorithmic fairness techniques** provide mathematical definitions and methods for reducing bias. These include pre-processing methods that transform data to remove correlations between sensitive attributes and other features, in-processing methods that add fairness constraints or regularization terms to the training objective, and post-processing methods that adjust model outputs to satisfy fairness criteria.

**Evaluation frameworks** should mandate disaggregated performance metrics across demographic groups. Fairness checklists and bias audits help teams systematically assess potential harms before deployment. Benchmark datasets specifically designed to test for bias, such as those measuring performance on dialect recognition or facial recognition across skin tones, provide standardized assessment tools.

**Governance and oversight** structures ensure accountability. Diverse and interdisciplinary teams are better positioned to identify potential biases that homogeneous groups might overlook. Documentation practices that record data provenance, modeling choices, and known limitations support transparency and due diligence.

**Continuous monitoring** after deployment is critical because bias can emerge or worsen as models interact with real-world data over time. Feedback loops, user reporting mechanisms, and periodic retraining with updated data help maintain fairness as conditions change.

## Related

- [[Fairness in Machine Learning]] - The broader field concerned with equitable outcomes in ML systems
- [[Algorithmic Accountability]] - Principles and practices for holding algorithms responsible for their impacts
- [[Data Ethics]] - Ethical considerations surrounding data collection, use, and governance
- [[Discriminatory AI]] - AI systems that produce biased or discriminatory outcomes
- [[Transparency in AI]] - Making AI decision-making processes understandable and open to scrutiny
