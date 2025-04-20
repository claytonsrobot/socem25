# Welcome to the SOCEM Project
The AgMEQ laboratory, under Dr. Daniel Robertson at the University of Idaho has been developing the SOCEM device since 2018.
The SOCEM device is meant to assess the characteristic fexural rigidity (EI) of wheat crops in the field.
Raw fore data, stem density data, and the health of contact is used to assess EI.

# SOCEM software
Previously referred to as Stemberry, this Socem software package is run on a Rasperry Pi.
An Arduino unit is connected via USB, to pass the live data feed to the Rasperry Pi via serial connection.

# How to run
> git clone https://github.com/claytonsrobot/socem25 # Adjust for the AgMECH github
> cd socem25 
> poetry install
> poetry run python -m src
> poetry run python run.py --mode shell
> poetry run python run.py --mode gui
> poetry run python run.py --mode api
> poetry run python -m socem25.shell.main
> poetry run python -m socem25.gui.main
> poetry run python -m socem25.api.main


# Shell functionality
> poetry run python -m shell

