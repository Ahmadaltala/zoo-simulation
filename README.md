# Zoo Simulation with Starvation and Deadlock Demonstration

This project simulates a Zoo with three gates and two visiting options (Open Area and Theater). It showes scenarios of starvation and deadlock using threads and provides solutions to resolve these issues.

## Features
- Simulates visitor entry through three gates with priority based queues.
- uses starvation by showing how lower-priority visitors for exmaple Regular would have wait forever.
- uses deadlock by simulating visitors requesting both resources (Open Area and Theater) with varying lock acquisition orders.
- Implements solutions to resolve starvation using an aging mechanism.
- Resolves deadlock by ensuring proper lock acquisition order.
- Tracks visitors currently inside the Zoo using a `visitors_in_zoo` list.

## Requirements
- Python 3.8 or higher

## Setup
1. Clone the repository.
2. Install the required libraries using:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the simulation using:
   ```bash
   python main.py
   ```

## Files
- `main.py`: Contains the main simulation logic, including starvation and deadlock demonstrations and their resolutions.
- `requirements.txt`: Lists the required Python libraries.
- `README.md`: Project documentation.

## How to Use
1. Run the program to simulate the Zoo.
2. Observe the output to understand starvation and deadlock scenarios.
3. Review the solutions implemented to resolve these issues.
4. Check the `visitors_in_zoo` list in the code to track visitors currently inside the Zoo.

## License
This project is for educational purposes.