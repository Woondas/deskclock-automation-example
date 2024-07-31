# MOXYMIND

## Requirements

To set up and run this project, you will need the following:

- Command Line Tools for Android
- An Android emulator or a real device - Configuration for the device can be set in the `config.yaml` file located in the `config` directory.

## Python Environment
pip install pipenv

Configure Environment Variables
When working on multiple Python projects, it's crucial to keep dependencies isolated to avoid conflicts and ensure consistency. One way to achieve this is by configuring Pipenv to create virtual environments within your project directory. This can be done by setting the environment variable.

setx PIPENV_VENV_IN_PROJECT 1

This configuration ensures that the virtual environment will be created within your project directory instead of the default location.

When managing a Python project, it's important to maintain a Pipfile and Pipfile.lock to ensure consistent dependency management. These files keep track of the packages your project depends on and their specific versions, providing a reliable environment setup for all.

To correctly add a package to your project and update the Pipfile and Pipfile.lock

pipenv install --ignore-pipfile --verbose
This command guarantees that the dependencies specified in the Pipfile.lock are installed, ignoring the Pipfile. This approach ensures that all installed packages match the exact versions and dependencies recorded in the Pipfile.lock, providing consistency and stability across all development environments and deployments.

## Run the tests suit:

pytest

## Test Report

After each test run, a `report.html` file is generated with the test results.