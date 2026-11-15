"""
This module contains the WeatherDataProcessor class for processing weather
station data. It supports loading weather observations from a CSV file,
extracting structured measurements (Temperature, Rainfall, Pollution_level)
from free-text message strings, and preparing the data for downstream
analysis and validation.

Usage:
    config_params = {
        'weather_csv_path': 'https://example.com/weather_data.csv',
    }
    processor = WeatherDataProcessor(config_params, logging_level="INFO")
    processor.process()
    df = processor.weather_df
"""

import re
import numpy as np
import pandas as pd
import logging
from data_ingestion import read_from_web_CSV


class WeatherDataProcessor:
    """
    A class for processing weather station data including data ingestion,
    measurement extraction from free-text messages, and preparation for
    validation checks.

    Attributes:
        weather_station_data (str): Path or URL to the weather station CSV file.
        patterns (dict): Patterns used internally for extracting measurements.
        weather_df (DataFrame): DataFrame holding the processed weather data.
        logger (Logger): Logger for runtime messages.

    Methods:
        initialize_logging(logging_level): Sets up logging.
        weather_station_mapping(): Loads weather station data from CSV.
        extract_measurement(message): Extracts a measurement from a message.
        process_messages(): Processes all messages to extract measurements.
        process(): Executes the full data processing pipeline.
    """

    def __init__(self, config_params, logging_level="INFO"):
        """
        Initialize the WeatherDataProcessor.

        Parameters
        ----------
        config_params : dict
            Configuration dictionary. Must contain 'weather_csv_path'.
        logging_level : str, optional
            Logging verbosity: 'DEBUG', 'INFO', or 'NONE'. Default is 'INFO'.
        """
        self.weather_station_data = config_params['weather_csv_path']
        self.patterns = {
            'Rainfall': r'(\d+(\.\d+)?)\s?mm',
            'Temperature': r'(\d+(\.\d+)?)\s?C',
            'Pollution_level': (
                r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
            ),
        }
        self.weather_df = None
        self.initialize_logging(logging_level)

    def initialize_logging(self, logging_level):
        """
        Set up logging for this instance of WeatherDataProcessor.

        Parameters
        ----------
        logging_level : str
            Logging verbosity: 'DEBUG', 'INFO', or 'NONE'.
        """
        logger_name = __name__ + ".WeatherDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False

        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO

        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            ch = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def weather_station_mapping(self):
        """
        Load weather station data from the configured CSV URL into weather_df.

        Uses the read_from_web_CSV utility to fetch and load data, then stores
        the result in the weather_df attribute.
        """
        self.weather_df = read_from_web_CSV(self.weather_station_data)
        self.logger.info(
            "Successfully loaded weather station data from the web."
        )

    def extract_measurement(self, message):
        """
        Extract a measurement key and numeric value from a message string.

        Parameters
        ----------
        message : str
            The message string containing measurement information.

        Returns
        -------
        tuple
            A tuple of (measurement_key, value) if a match is found;
            otherwise (None, None).
        """
        for key, pattern in self.patterns.items():
            match = re.search(pattern, message)
            if match:
                self.logger.debug(f"Measurement extracted: {key}")
                return key, float(
                    next(x for x in match.groups() if x is not None)
                )
        self.logger.debug("No measurement match found.")
        return None, None

    def process_messages(self):
        """
        Process all messages in weather_df to extract measurements.

        Adds 'Measurement' and 'Value' columns to weather_df.

        Returns
        -------
        DataFrame
            The modified weather_df with extracted measurements.
        """
        if self.weather_df is not None:
            result = self.weather_df['Message'].apply(
                self.extract_measurement
            )
            self.weather_df['Measurement'], self.weather_df['Value'] = zip(
                *result
            )
            self.logger.info(
                "Messages processed and measurements extracted."
            )
        else:
            self.logger.warning(
                "weather_df is not initialized, skipping message processing."
            )
        return self.weather_df

    def process(self):
        """
        Execute the full data processing pipeline.

        Loads weather station data, then processes messages to extract
        structured measurements.
        """
        self.weather_station_mapping()
        self.process_messages()
        self.logger.info("Data processing completed.")
