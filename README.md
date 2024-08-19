# Real-Time Chat Application
## Overview
This project is a real-time chat application designed to facilitate instant messaging between users. The application supports secure user sessions, efficient data storage, and seamless communication across devices.

**Features**

**Real-Time Communication:** Leveraged WebSockets to enable instant messaging between users.

**JWT Authentication:** Implemented JSON Web Token (JWT) for secure user authentication and session management.

**Message Transfer:** Used Axios for efficient communication between the frontend and backend, ensuring smooth data flow.

**Database Management:** Utilized SQLAlchemy for managing the application's database, providing robust support for data storage and retrieval.

**Responsive UI:** Designed a dynamic and responsive user interface with HTML, CSS, and JavaScript, ensuring compatibility across various devices.

## Technologies Used

**Frontend:** React.js, HTML, CSS, JavaScript

**Backend:** FastAPI, WebSockets, SQLAlchemy, JWT

**Communication:** Axios

Installation

Prerequisites

Python 3.x

Node.js & npm

PostgreSQL (or any preferred SQL database)

**Backend Setup**

**Clone the repository:**

git clone https://github.com/your-username/chat-app.git

cd chat-app/backend

**Create a virtual environment and activate it:**

python3 -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

**Install the required dependencies:**

pip install -r requirements.txt

**Set up the database:**

## Replace `DATABASE_URL` with your actual database URL

export DATABASE_URL='postgresql://user:password@localhost/chat_db'

python manage.py migrate

**Run the FastAPI server:**

uvicorn main:app --reload

Frontend Setup

**Navigate to the frontend directory:**
cd ../frontend

**Install the dependencies:**

npm install

**Start the development server:**

bash

Copy code

npm start

Usage

Open the application in your browser:

http://localhost:3000

Register or log in to start chatting in real-time with other users.
