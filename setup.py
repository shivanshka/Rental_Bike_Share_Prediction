from setuptools import find_packages, setup
from typing import List

# Declaring Variables for setup functions
PROJECT_NAME = "Rental-Bike-Share-Demand-Prediction"
VERSION = "0.0.1ins"
AUTHOR = "Shivansh Kaushal and Chirag Sharma"
DESCRIPTION = "This application predicts the demand for shared bike in Washington DC for given conditions"
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirements_list()->List[str]:
    """
    Description: This function is going to return list of requirement mentioned in requirements.txt
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")

setup(
    name = PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
#    install_requires=get_requirements_list()
)

#if __name__=="__main__":
#    print(get_requirements_list())


