# Molecule.i

## Overview

Welcome to the Molecule.i! This project was for a school assignemnt aimed at creating a platform to display molecules from an SDF (Structure Data File) format to an SVG (Scalable Vector Graphics) format. The website is designed to facilitate the visualization of molecular structures in 3D, making it a valuable tool for chemistry enthusiasts, students, and professionals.

## Features

- **SDF to SVG Conversion:** The website allows users to upload an SDF file containing molecular data, and the backend processes it to generate an SVG representation for easy visualization.

- **Colour choices for Atoms** The website allows users to choose the specific colour they want each atom e.g. Hydrogen or Oxygen to be to make the most colourful molecule images.

- **C and Python Backend:** The backend of the application is developed using both C and Python programming languages. C is employed for efficient data processing, while Python wraps around the C functions using SWIG for the complex molecule SDF parsing, SQLite database connection and communication, generating SVG files and http server setup and running.

- **SQLite Database:** The application utilizes an SQLite database to store sdf files, element colour information and tables representing each molecule.

- **HTML/CSS and jQuery Frontend:** The frontend of the website is built using HTML and CSS for structure and styling. jQuery is used to enhance user interactions, providing a smooth and dynamic user experience, and, communication with the python server.

## Languages used
![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![JQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)

## Running the program
- Download python and SWIG if not yet available in your system
- Enter in command line:   
```
make  
export LD_LIBRARY_PATH=.  
python3 server 8000  
```
- Open a browser and enter: http://localhost:8000/index.html


