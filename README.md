## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Run tests:
   ```
   python manage.py test
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/shorten/` - Create a new shortened URL
  ```json
  {
    "original_url": "https://example.com"
  }
  ```
  Response:
  ```json
  {
    "shortened_url": "http://domain.com/abc123"
  }
  ```

- `GET /<short_code>/` - Redirect to the original URL
  - No request body needed
  - Redirects to the original URL

- `DELETE /api/shorten/{id}/` - Delete a shortened URL
  - No request body needed
  - No response body
