<div align="center">
  <img src="https://github.com/HohShenYien/caringly/assets/55322546/c879ecfb-a09f-468a-b598-ceeb440adac2" alt="Caringly Logo">
</div>

<h1 align="center">
  Caringly
</h1>

<p align="center">
  Reminding you to care for those whom you love.
</p>

![VdTdB7h](https://github.com/HohShenYien/caringly/assets/55322546/72db1bb1-c5a5-4734-97eb-d7ce13cad242)

Caringly is my **Final Year Project** for Asia Pacific University's BSc (Hons) in Computer Science (Data Analytics). This repository contains the **backend** codes of the project, built using [Flask](https://flask.palletsprojects.com/en/2.3.x/).

Its goal is to allow users to **monitor** the social media posts of those they care for. Using deep learning sentiment analysis model, it will analyze signs of depression/suicide from the texts and send alert emails to users if any sign is detected

## ⚡ Features

- 🤖 **Classifies** texts into neutral, suicidal, or depressive with a high accuracy (82%).
- 📬 **Retrieves Social Media** (Instagram & Twitter) posts using unofficial APIs
- ⏰ An hourly **scheduled** task for posts retrieval
- ✉ Alerts users using **Email**
- 🔒 Basic **Authentication** using JWT

## 👨‍🔬 Model

- 🔃 Uses a **two-step** classification model to classify the texts
- ✅ First Model detects if the texts are **dangerous** (non-neutral) at an F1-score of **0.98**
- ⚠ Second Model detects if the texts are **suicidal** or **depressive** at an F1-score of **0.77**
- 🚀 First Model is an **LSTM** model while the second uses **bi-LSTM**.
- 📂 The models can be found in `/server/scan/models/`
- 📕 The notebook is in `/assignment-notebook.ipynb`

Check out the backend codes at [caringly](https://github.com/HohShenYien/caringly)
