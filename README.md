# E-Commerce API

A modern, full-featured REST API for an e-commerce platform built with FastAPI, SQLAlchemy, and PostgreSQL. This application provides comprehensive functionality for product management, user authentication, shopping cart operations, payment processing, and sales tracking.

## Features

- **Product Management**: Add, retrieve, and manage products with categories and discounts
- **User Authentication**: Secure user registration and login with JWT tokens
- **Shopping Cart & Checkout**: Complete checkout workflow with cart management
- **Payment Processing**: Integrated payment gateway for transactions
- **Sales Tracking**: Monitor sales and top-selling products
- **Currency Support**: Multi-currency support with country-based conversion
- **Image Storage**: Google Drive integration for product image uploads
- **Database**: PostgreSQL backend with SQLAlchemy ORM

## Project Structure

```
├── config/                    # Configuration modules
│   ├── database.py           # Database connection setup
│   ├── drive_configuration.py # Google Drive integration
│   ├── get_drive_id_for_folder.py
│   ├── payment_auth.py       # Payment authentication
│   └── quickstart.py
├── models/                    # SQLAlchemy ORM models
│   └── models.py            # Database models (Product, User, etc.)
├── routers/                   # API endpoints
│   ├── checkout.py          # Checkout operations
│   ├── home.py              # Home page endpoints
│   ├── payment.py           # Payment endpoints
│   ├── sales.py             # Sales tracking
│   ├── store.py             # Store/product endpoints
│   ├── users.py             # User management
│   └── sessions.py          # Session management
├── schemas/                   # Pydantic schemas for request/response validation
│   └── schema.py
├── utils/                     # Utility functions
│   ├── currency.py          # Currency conversion utilities
│   └── utils.py
├── database/
│   └── database.sql         # Database schema
├── main.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── credentials.json          # Google Cloud credentials

```

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: python-jose, bcrypt
- **File Storage**: Google Drive API
- **Server**: Uvicorn
- **Utilities**: python-dotenv, requests

## Requirements

- Python 3.8+
- PostgreSQL
- Google Cloud Project with Drive API enabled

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Ecommerce
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Unix/MacOS
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Google Drive Storage**

   1. Go to [Google Cloud Console](https://console.cloud.google.com/welcome?project=ecommerce-470214)
   2. Create a new project from the navigation menu
   3. Click on **APIs & Services**
   4. Create a new OAuth 2.0 credential and download the JSON file
   5. Save it as `credentials.json` in the project root
   6. Add your Authorized redirect URIs to the client configuration

5. **Database Setup**
   - Create a PostgreSQL database
   - Update connection string in `config/database.py`
   - Run the schema from `database/database.sql`

6. **Environment Configuration**
   - Create a `.env` file in the project root
   - Add necessary environment variables (database URL, API keys, etc.)

## Running the Application

Start the development server:

```bash
python main.py
```

Or directly with uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Routes

### Products
- `POST /users/add/product` - Add a new product
- Store endpoints for product retrieval and management

### Users
- User registration and management endpoints

### Checkout
- Cart management and checkout operations

### Payment
- Payment processing and transaction handling

### Sales
- Sales tracking and analytics

### Home
- Home page endpoints with featured and discounted products

### Currency
- Currency conversion based on user location

## Key Models

### Product
- id, name, brand, price, stock_quantity
- category, sub_category, discount
- product_image_url (stored in Google Drive)
- quantity_sold, currency

### User
- User authentication and profile information

### Order/Transaction
- Order tracking and payment information

## Security

- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt for secure password storage
- **HTTPS**: Recommended for production deployment

## Dependencies

```
fastapi
SQLAlchemy
google-auth
uvicorn
python-dotenv
psycopg2-binary
bcrypt
python-jose
python-multipart
requests
google-api-python-client
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License

## Support

For issues or questions, please create an issue in the repository.
