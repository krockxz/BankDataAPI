Here's the updated and properly formatted README file:

```markdown
# Bank Branch API Service

This project provides a web service for querying bank and branch data using both GraphQL and REST APIs. The service is built using Python and Flask and interacts with an SQLite database to retrieve bank and branch details.

## Features

- **GraphQL API**: Allows querying of bank branches with associated bank details.
- **REST API**: Provides endpoints to retrieve the list of banks and specific branch details.
- **SQLite Database**: Stores bank and branch information.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `venv` for virtual environment management

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   ```

2. **Activate the virtual environment**:

   If you already have a virtual environment set up, activate it:

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. **Install the dependencies**:

   Install the required Python packages using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the SQLite database**:

   Run the following script to create the SQLite database and insert the necessary data:

   ```bash
   python data_insertion.py
   ```

   This will create a file named `database.sqlite3` in the project directory, containing the bank and branch data.

### Running the Server

Start the Flask server with the following command:

```bash
python app.py
```

The server will start on `http://localhost:5000/`.

## Running Tests

To ensure everything is working correctly, you can run the included unit tests.

1. **Activate the virtual environment** if it is not already activated:

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

2. **Run the tests**:

   Use the following command to run the tests:

   ```bash
   python -m unittest discover -s tests
   ```

   This will execute all tests in the `tests` directory.

## API Endpoints

### GraphQL API

- **Endpoint**: `/gql`
- **Sample Query**: 

  To retrieve all branches with their associated bank details, you can use the following GraphQL query:

  ```graphql
  query {
      branches {
          edges {
              node {
                  branch
                  bank {
                      name
                  }
                  ifsc
              }
          }
      }
  }
  ```

  **Test with `curl`**:

  ```bash
  curl --location 'http://localhost:5000/gql' \
  --header 'Content-Type: application/json' \
  --data '{"query":"{ branches { edges { node { branch bank { name } ifsc } } } }","variables":{}}'
  ```
