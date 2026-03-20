<p align="center">
  <a href="" rel="noopener">
</a>
</p>

<h1 align="center">Address Book Backend Server</h1>

---

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

This is a backend application implemented in FastAPI to provide CRUD functions to Addresses. The address data contains the following fields:

<ul>
    <li><strong>label</strong> - this is an optional custom tag for each address</li>
    <li><strong>houseNo</strong> - house/lot/unit number</li>
    <li><strong>street</strong> - street name</li>
    <li><strong>city</strong> - city/province name</li>
    <li><strong>barangay</strong></li>
    <li><strong>region</strong></li>
    <li><strong>country</strong></li>
    <li><strong>latitude</strong> - numerical data that defines the north-south position on the earth's grid</li>
    <li><strong>longitude</strong> - numerical data that defines the east-west position on the earth's grid</li>
</ul>
The database is currently stored in an aqlite file.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

Make sure you you have <strong>Python 3.10+</strong> installed

To check, run this in cmd:

```
python --version
```

It should return the verion of Python installed on your device. Otherwise, click this [link](https://www.python.org/downloads/) to download Python

### Installing

1.) Clone this repository

```
git clone https://github.com/Kashkanov/AddressBook.git
cd AddressBook
```

2.) Create a python environment using cmd.

```
python -m venv .venv
```

Once created, you can activate it with the command:

```
.venv\Scripts\activate
```

To deactivate, run

```
deactivate
```

3.) Activate the virtual environment then install the dependencies

```
pip install -r requirements.txt
```

4.) Set up environment variables
Create a .env file on project root containing the following:

```
DATABASE_URL=sqlite:///./address_book.db
```

5.) Run the application

```
uvicorn main:app --reload
```

The application is accessible at http://localhost:8000.

## 🔧 Running the tests <a name = "tests"></a>

To perform testing, make sure that the virtual environment is activated, then run

```
pytest
```

The tests use a different database that wipes itself after every test run. Testing does not affect the main database.

## 🎈 Usage <a name="usage"></a>

All endpoints can be explored and tested via the Swagger UI at http://localhost:8000/docs after running the application.

## 🚀 Deployment <a name = "deployment"></a>

A Dockerfile is present for Docker deployment.

Build the image:

```
docker build -t address-book .
```

Run the container:

```
docker run -p 8000:8000 address-book
```

Once again, the application is running on http://localhost:8000.

## ⛏️ Built Using <a name = "built_using"></a>

- FastAPI — web framework for building the REST API
- SQLAlchemy — ORM for database access and table management
- SQLite — lightweight file-based database for local storage
- Pydantic — data validation and request/response schemas
- geopy — geodesic distance calculations for the nearby search feature
- Uvicorn — ASGI server for running the application
- pydantic-settings — environment variable and .env file configuration

## ✍️ Authors <a name = "authors"></a>

- [@kashkanov](https://github.com/Kashkanov/)
