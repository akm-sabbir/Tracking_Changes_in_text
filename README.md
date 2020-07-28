# FastAPI Python Template #

This repository contains a template project using FastApi framework for Python

### What is this repository for? ###

This is a template for FastApi projects to use as a reference

### How do I get set up? ###

1. First, set up a Python virtual environment and activate it.
2. Then run the following command to setup the dependencies:
`
python run.py setup
`
3. Run `main.py` to start the server

### Rest Endpoints and routers ###
The REST endpoints available for this project are:

1. http://localhost:8080/externalApi
2. http://localhost:8080/calculator

For more info about request methods and sub-routes, check the Swagger URL below.

The `router` package has all the FastApi routers for this project. Please refer to them when creating new endpoints.

You do need need to add routers to the app. The `main.py` script searches the `router` package and adds them automatically to the FastApi app.

### Exception Handling ###
The `exception` package has all needed classes for Exception Handling. The `ServiceException` class is a custom `Exception` that is thrown in the application. This class `ExceptionResponseFactory` creates a response for the error that occurs. 

If an exception is thrown in multiple places in the application, please add a handler for the exception in `ExceptionHandler` class. 

### Logging ###
Logging and log levels are controlled by the `logging.ini` file. Make changes in the files to adjust log output, file name, rollout policy and log levels for each environment.

### API Documentation with Swagger ###
FastApi has swagger built in.

Link to Swagger UI: http://localhost:8080/docs

### External API Calls ###
Use methods from class `RestClientUtil` class to make external calls. Please refer to the class for making external calls.

### Configuration Management ###
The class `ConfigManager` in `util` package manages all the configuration. Use the methods in this class to access a configuration. The `config.ini` file contains all the configs for the app. 