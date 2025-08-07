import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

db_password = os.getenv("PASSWORD")


try:
    conn = psycopg2.connect(
        database = "E-COMMERCE",
        user = "postgres",
        password = db_password,
        host = "localhost",
        port = "5432"
    )

    cursor = conn.cursor(cursor_factory = RealDictCursor)

    cursor.execute("""
    
    DO $$
    BEGIN 
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE pg_type.typname = 'list_gender') THEN 
            CREATE TYPE list_gender AS ENUM ('male','female');
        END IF;
    END
    $$;
                   
    CREATE TABLE IF NOT EXISTS dim_product(
        id SERIAL PRIMARY KEY,
        name VARCHAR(300),
        brand VARCHAR(300),
        price INT,
        stock_quantity INT,
        category VARCHAR(300),
        sub_category VARCHAR(200),
        product_image BYTEA,
        date_added TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                   );

    CREATE TABLE IF NOT EXISTS dim_customers(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(300),
        last_name VARCHAR(300),
        email VARCHAR(300),
        gender list_gender,
        age INT,
        password VARCHAR(100),
        signup_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP                      
                   );
    
    CREATE TABLE IF NOT EXISTS dim_date(
        id SERIAL PRIMARY KEY,
        date VARCHAR(300),
        day VARCHAR(100),
        month VARCHAR(200),
        quarter INT,
        year INT,
        weekday VARCHAR(100)
    );
    DO $$
    BEGIN
        IF NOT EXISTS(SELECT 1 FROM pg_type WHERE pg_type.typname = 'shipping') THEN
            CREATE TYPE shipping AS ENUM ('standard','express','same-day');
        END IF;
    END
    $$;
                   
    CREATE TABLE IF NOT EXISTS dim_shipping(
        id SERIAL PRIMARY KEY,
        shipping_type shipping,
        shipping_cost INT,
        carrier_name VARCHAR(200),
        delivery_time_days INT           
                   );
    CREATE TABLE IF NOT EXISTS dim_store(
        id SERIAL PRIMARY KEY,
        store_name VARCHAR(200),
        location VARCHAR(200),
        manager VARCHAR(200)
                   );      
    DO $$
    BEGIN
        IF NOT EXISTS(SELECT 1 FROM pg_type WHERE pg_type.typname = 'payment') THEN
            CREATE TYPE payment AS ENUM('credit_card','cancelled','refunded');
        END IF;
    END
    $$;
    
    DO $$
    BEGIN
        IF NOT EXISTS(SELECT 1 FROM pg_type WHERE pg_type.typname = 'sales_status') THEN
            CREATE TYPE status AS ENUM ('completed','cancelled','refunded');
        END IF;
    END
    $$;
    CREATE TABLE IF NOT EXISTS fact_sales(
        id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        product_id INT NOT NULL,
        date_id INT NOT NULL,
        payment_method payment,
        quantity INT,
        unit_price INT,
        dicount INT,
        total_amount INT,
        status sales_status,
        FOREIGN KEY (customer_id) REFERENCES dim_customers(id),
        FOREIGN KEY (product_id) REFERENCES dim_product(id),
        FOREIGN KEY(date_id) REFERENCES dim_date(id)
        );         
                   
    ALTER TABLE dim_product ADD COLUMN IF NOT EXISTS product_image BYTEA;
    ALTER TABLE dim_customers ADD COLUMN IF NOT EXISTS password VARCHAR(100);
  
    """
    )

    conn.commit()
    

except psycopg2.errors as e:
    print("Error initializing the database")


