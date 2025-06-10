# bship
battleship project

setup venv
    - python -m venv venv 3.10.7
    - venve\Scripcts\activate
    - pip install -r "requirements.txt"

setup concurrently
    - npm install --save-dev concurrently


run backend
    - either
     |  cd path/to/bship/backend
     |  uvicorn main:app --reload
    - or
     |  uvicorn backend.main:app --reload

run frontend
    cd path/to/bship/frontend
    npm start

run project
    cd path/to/bship/frontend
    npm run dev


.\venv\Scripts\activate