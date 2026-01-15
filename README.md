# Late Show API

A simple Flask REST API for managing episodes, guests, and appearances on a late-night talk show.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Seed the database:
```bash
python seed.py
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5555`

## API Endpoints

### GET /episodes
Returns all episodes.

**Response:**
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  }
]
```

### GET /episodes/:id
Returns a specific episode with its appearances.

**Response (Success):**
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      },
      "guest_id": 1,
      "id": 1,
      "rating": 4
    }
  ]
}
```

**Response (Not Found):**
```json
{
  "error": "Episode not found"
}
```

### GET /guests
Returns all guests.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  }
]
```

### POST /appearances
Creates a new appearance linking a guest to an episode.

**Request Body:**
```json
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}
```

**Response (Success):**
```json
{
  "id": 4,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

**Response (Validation Error):**
```json
{
  "errors": ["Rating must be between 1 and 5"]
}
```

## Testing

Use the provided Postman collection (`challenge-4-lateshow.postman_collection.json`) to test all endpoints:

1. Import the collection into Postman
2. Ensure the server is running on `http://localhost:5555`
3. Test each endpoint to verify functionality

## Data Model

- **Episode**: id, date, number
- **Guest**: id, name, occupation  
- **Appearance**: id, rating (1-5), episode_id, guest_id

### Relationships

- An Episode has many Guests through Appearances
- A Guest has many Episodes through Appearances  
- An Appearance belongs to both an Episode and a Guest