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

#### Setting up the Server

1. Navigate to the `Server` folder.
    ```
    cd Server
    ```
2. Install the required Python dependencies.
    ```
    pip install -r requirements.txt
    ```
3. Navigate to the `src` folder.
    ```
    cd src
    ```
4. Run the Flask server.
    ```
    Python .\Flask_app.py
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
3. Create a new database for the project:
    ```
    CREATE DATABASE your_database_name;
    ```
4. Select the database you created:
    ```
    USE your_database_name;
    ```
5. Import the `.sql` file located in the MySQL folder to create the required tables:
    ```
    SOURCE MySQL/setup.sql;
    ```