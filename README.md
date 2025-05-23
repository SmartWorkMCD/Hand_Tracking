# Hand_Tracking
Repository for the hand tracking microservice of the SmartWorkMCD project 2024/25 UA

## Module Description

### Description:
- Uses computer vision to detect worker hand positions and gestures during
assembly.
- Helps determine whether the worker’s actions align with the expected workflow.

### Functionality:
- Captures images using a camera and processes them using AI models.
- Detects hand movements and verifies interactions with the components.
- Sends data to the Workstation Brain for task completion validation or alerts (e.g.,
when incorrect actions are detected).

### Responsible Members:
- Main Responsible: Hugo Veríssimo
- Team: Hugo Veríssimo, Pedro Mendes, Pedro Batista

## Running the App

To run the app locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/SmartWorkMCD/Hand_Tracking.git
    cd Hand_Tracking
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On macOS/Linux
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run Neighbooring Components (The module migth require another module to be runnning)**
    ```sh
    docker compose up
    ```

5. **Run the app**:
    ```sh
    python3 app/main.py
    ```

## Running the Tests

To run the tests, follow these steps:

1. **Ensure the virtual environment is activated**:
    ```sh
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On macOS/Linux
    ```

2. **Run the tests using pytest**:
    ```sh
    pytest
    ```

## Contribution Guidelines

To ensure a smooth collaboration, please follow these guidelines:

1. **Do not push directly to the `main` branch**: All changes should be made through pull requests.
2. **Submit pull requests to the `development` branch**: Create a new branch for your feature or bug fix and submit a pull request to the `development` branch.
3. **Write clear commit messages**: Use descriptive commit messages that explain the purpose of the changes.
4. **Run tests before submitting a pull request**: Ensure that all tests pass and that your changes do not introduce any new issues.
5. **Follow the coding standards**: Maintain consistent coding style and adhere to the project's coding standards.

### Example Workflow

1. **Create a new branch**:
    ```sh
    git checkout -b feature/my-new-feature
    ```

2. **Make your changes and commit them**:
    ```sh
    git add .
    git commit -m "Add new feature"
    ```

3. **Push your branch to GitHub**:
    ```sh
    git push origin feature/my-new-feature
    ```

4. **Create a pull request**: Go to the GitHub repository and create a pull request to the `development` branch.

Thank you for contributing to the project!