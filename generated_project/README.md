# Integer Difference Calculator

A simple Python application that calculates the difference between two integers.

## Description

This project consists of a main application that prompts the user for two integers and displays their difference. The calculation logic is separated into a dedicated calculator module for better code organization and reusability.

## Project Structure

- `main.py` - Main application file that handles user input and output
- `calculator.py` - Module containing the difference calculation function
- `README.md` - This documentation file

## Requirements

- Python 3.x

## Usage

Run the main application:

```bash
python main.py
```

Or make it executable and run directly:

```bash
chmod +x main.py
./main.py
```

The application will prompt you to enter two integers and will display their difference.

## Example

```
Enter the first integer: 10
Enter the second integer: 3
The difference between 10 and 3 is: 7
```

## Using the Calculator Module

You can also import and use the calculator module in your own Python code:

```python
from calculator import calculate_difference

result = calculate_difference(10, 3)
print(result)  # Output: 7
```

## Features

- Simple and intuitive command-line interface
- Input validation and error handling
- Modular design for easy maintenance and testing
- Clear documentation and usage instructions

## License

This project is open source and available for educational purposes.
