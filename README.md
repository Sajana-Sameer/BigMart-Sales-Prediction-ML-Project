# BigMart Sales Prediction End to End Project
# BigMart Sale Prediction

![BigMart Sale Prediction](./static/bigmart.webp)

## Table of Contents

- [Introduction](#introduction)
- [Project Description](#project-description)
- [Directory Structure](#directory-structure)
- [Data](#data)
- [Installation](#installation)
- [Usage](#usage)
- [Model Training](#model-training)
- [Prediction](#prediction)
- [Data Preprocessing](#Data-Preprocessing)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This is an end-to-end machine learning project for predicting the sales of products in BigMart stores. The goal of this project is to develop a predictive model that can assist BigMart in optimizing their inventory and making data-driven decisions to increase sales and revenue.

## Project Description

BigMart Sale Prediction project is divided into several components:

- **Data Ingestion:** The data from various sources, such as CSV files, is loaded into the system for further processing.

- **Data Transformation:** Data preprocessing and feature engineering are performed to prepare the data for model training.

- **Model Training:** Machine learning models are trained on the preprocessed data to predict product sales.

- **Prediction:** The trained model is deployed in a web application, where users can input product details, and the application will provide sales predictions.

## Directory Structure

The project has the following directory structure:
Dictionary Tree
```
├── artifacts/
│   ├── data.csv
│   ├── test.csv
│   ├── train.csv
│   ├── model.pkl
│   └── proprocessor.pkl
├── notebook/
│   ├── data/
│   └── Bigmart sales prediction.ipynb
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── predict_pipeline.py
│   │   └── train_pipeline.py
│   ├── __init__.py
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
├── static/
│   ├── log1.jpg
│   ├── download.png
│   └── bigmart.webp
├── templates
│   ├── home.html
│   └── index.html
├── requirements.txt
├── app.py
├── streamlit_app.py
├── setup.py
├── LICENSE
└── README.md
```
## Data

The project uses two main datasets:

- `train.csv`: This dataset contains historical sales data with features like product type, weight, and store location.

- `test.csv`: This dataset is used to evaluate the model's performance and make predictions for future sales.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/BigMart-Sale-Prediction.git`
2. Navigate to the project directory: `cd BigMart-Sale-Prediction`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage
## Usage
( Note: I have initially written the code using Flask for learning purposes, but I have now used Streamlit to deploy the application.)

To run the BigMart Sale Prediction web application, follow these steps:

1. First, make sure you have installed the required dependencies by running the following command:

   ```bash
   pip install streamlit

Once the dependencies are installed, you can run the web application using the following command:

bash


   ```bash
   streamlit run app.py
   ```

The web application will be accessible at http://localhost:8501.

pen your web browser and navigate to this URL to access the application.

Now, users can use the web form to input product details and get the predicted sales for the product.

## Model Training

To retrain the machine learning model, you can use the `src/pipeline/train_pipeline.py` script. Adjust the script to suit your specific model and training requirements.

## Prediction

The web application provides a user interface for making sales predictions. Users can input product details, and the application will display the predicted sales for the product.

## Data Preprocessing

The project utilizes the following data preprocessing techniques:

- One-Hot Encoding: Convert categorical variables into binary vectors to handle categorical data in the machine learning model.
- Label Encoding: Encode categorical variables into numeric format for model training.
- StandardScaler: Scale numeric features to have mean=0 and variance=1, ensuring the features are on a similar scale.

## Technologies Used

The project uses the following technologies:

- Python
- Streamlit
- Pandas
- Scikit-learn
- NumPy
- Matplotlib
- Seaborn
- Flask
- HTML/CSS
- JavaScript

## Contributing

Contributions to the project are welcome. If you find any issues or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Contact

For any inquiries or questions, you can reach out to the project maintainer:

- Name: Sajana Sameer
- Email: sajjusam2014@gmail.com

Feel free to update the above details with your specific project information. 