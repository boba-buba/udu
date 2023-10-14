import mysql
from mysql.connector import errorcode
import logging
import  time
from db_config import config

import csv, os


class db_connection:

    temp_result = []
    def set_up_logger(self):
        # Set up logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Log to console
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Also log to a file
        file_handler = logging.FileHandler(".\\cpy-errors.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger


    def connect_to_mysql(self, conf, attempts=3, delay=2):
        logger = self.set_up_logger()
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**conf)
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    # Attempts to reconnect failed; returning None
                    logger.info("Failed to connect, exiting without a connection: %s", err)
                    return None
                logger.info(
                    "Connection failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    attempts-1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return None


    def insert_db(self, statement):

        try:
            cnx = self.connect_to_mysql(config, attempts=3)

            cursor = cnx.cursor()
            cursor.execute(statement)
            cnx.commit()
            print(cursor.rowcount, "Record(s) inserted successfully")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record {}".format(error))

        finally:
            if cnx.is_connected():
                cnx.close()
                print("MySQL connection is closed")

    def execute_query(self, query):

        try:
            cnx = self.connect_to_mysql(config, attempts=3)

            cursor = cnx.cursor()
            cursor.execute(query)
            self.temp_result = cursor.fetchall()
            cnx.commit()
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record {}".format(error))

        finally:
            if cnx.is_connected():
                cnx.close()
                print("MySQL connection is closed")








