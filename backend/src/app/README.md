1. Clone git repo
   git clone https://github.com/SoumyaBadola18/InApp-Assignment.git
   cd InApp-Assignment
   
3. Install project dependencies:

   pip install -r backend/requirements.txt

4. Prepare Dataset Folder:

   - Create a folder named "datasets" under the directory "InApp-Assignment/backend":

     mkdir backend/datasets

   - Download the following files and place them into the "datasets" folder:

     - https://datasets.imdbws.com/name.basics.tsv.gz
     - https://datasets.imdbws.com/title.basics.tsv.gz

2. Load Data into SQLite Database:

   Run the following script to populate the SQLite database with the datasets:

   python backend/app/load_data.py

3. Create a User for Authentication:

   Run the following command to create a user with username `admin` and password `password123`:

   python backend/app/create_user.py admin password123

4. Run the Flask API server:

   python backend/app/app.py

   The server will start on: http://127.0.0.1:5000

5. Generate JWT Token:

   Use the `/login` endpoint to get an authentication token. Example using `curl`:

   curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "password123"}'

   This will return a JSON response containing your JWT token:

   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
   }

6. Use Token in API Requests:

   For all subsequent requests, add the token in the Authorization header like this:

   Authorization: Bearer <your_token_here>

Example Endpoints
-----------------

8. Search for Movies:

   curl -X GET "http://127.0.0.1:5000/search/movie?year=2020" -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json"

9. Search for People:

   curl -X GET "http://127.0.0.1:5000/search/person?name=Tom" -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json"