Scoliaware

Overview
Scoliaware is an AI-powered tool designed to assess scoliosis severity from spinal X-rays. Using YOLO-based vertebra detection and automated Cobb angle calculation, it aims to provide quick, consistent, and interpretable measurements to support early diagnosis, especially in underserved communities with limited access to specialists.

Features
YOLO-based vertebra detection for accurate spine localization
Automatic Cobb angle computation with reference comparison
Modular pipeline allowing future integration with additional ML models

Impact
Scoliaware addresses gaps in accessibility and consistency of scoliosis assessment. Early testing on curated X-ray images demonstrates promising measurements, laying the groundwork for future validation, clinical support, and research applications. Accuracy is improving as the model is refined, highlighting iterative design and responsible AI development.

Technologies
Python, Streamlit, PIL, math
YOLOv8 for vertebra detection
Publicly available datasets for training and evaluation 

Usage
1.Input X-ray images into the pipeline
2.YOLO model detects vertebrae
3.Automatic Cobb angles are calculated and exported for review
