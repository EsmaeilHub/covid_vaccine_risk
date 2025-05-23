import os
import sys
from src.exception_handler import handle_exception
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
# from src.components.data_preprocessing import data_preprocessing

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer


from src.utils import fetch_kaggle_as_dataframe


@dataclass
class DataIngestionConfig:
    """
    Configuration class for data ingestion.

    This class defines the file paths used during the data ingestion process,
    including paths for the raw data, training data, and test data. The files
    are stored in the 'artifacts' directory.
    """

    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        try:
            df = fetch_kaggle_as_dataframe(
                kaggle_url="samxsam/human-cognitive-performance-analysis",
                file_name="human_cognitive_performance.csv"
            )
            logging.info("Read the dataset as dataframe")
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True
            )
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            df=df.iloc[:2000,:]
            logging.info("Limited data is in use!")

            # df = data_preprocessing(df)
            # logging.info("Preprocessing done")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise handle_exception(e)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_data_path, test_data_path
    )

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
