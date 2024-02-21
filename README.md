# Software Engineering Project Team 3

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed the latest version of [Node.js and npm](https://nodejs.org/).
- You have installed Python 3.11 or later.
- MySQL installed
- You have a Windows machine (this has only been tested on Windows, it may work on other operating systems).

### Installing

A step by step series of examples that tell you how to get a development environment running.

### Setting up the Server

Follow these steps to set up your server environment:

1. **Navigate to the `Server` folder.**
    ```bash
    cd Server
    ```

2. **Install the required Python dependencies.**
    ```bash
    pip install -r requirements.txt
    ```

3. **Create and populate a `.env` file with your database credentials.**
    Before running the Flask server, you'll need to create a `.env` file in the root directory to store sensitive information such as database credentials securely. This file is not tracked by version control.

    Create the `.env` file and add the following lines to it:

    ```plaintext
        EMAIL = "EMAIL USERNAME"
        PASSWORD = "EMAIL PASSWORD"
        SECRET_KEY = "SECRET ENCRPYTION KEY"
        DB_PASSWORD = "YOUR DATABASE PASSWORD"
    ```

5. **Run the Flask server.**
    ```bash
    python Flask_app.py
    ```

#### Setting up the Client

1. Navigate to the `Client` folder.
    ```
    cd Client
    ```
2. Install the necessary npm packages.
    ```
    npm install
    ```
3. Serve the Vue.js application.
    ```
    npm run dev
    ```
4. The Vue.js application will be running on [http://localhost:8080](http://localhost:8080) (or another port if 8080 is busy).

#### Setting Up the MySQL Database

1. Start your MySQL server on your local machine.
2. Open a MySQL client or use the command line to connect to your MySQL server.
3. Import the `.sql` dump file in the MySQL folder
### Running Tests Locally

To run unit tests, please refer to the `README.md` files in the `/Client` and `/Server` directory