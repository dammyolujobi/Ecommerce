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
        price DOUBLE PRECISION,
        stock_quantity INT,
        category VARCHAR(300),
        sub_category VARCHAR(200),
        discount DOUBLE PRECISION,
        product_image_url TEXT[] NOT NULL,
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
        sales_id INT,
        FOREIGN KEY (sales_id) REFERENCES fact_sales(id),
        signup_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP                      
                   );
    

    ALTER TABLE dim_customers
    ADD COLUMN IF NOT EXISTS sales_id INT;

    ALTER TABLE dim_customers
    ADD CONSTRAINT fk_sales
    FOREIGN KEY (sales_id) REFERENCES fact_sales(id);

    
    

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
        discount DOUBLE PRECISION,
        total_amount DOUBLE PRECISION,
        status sales_status,
        FOREIGN KEY (customer_id) REFERENCES dim_customers(id),
        FOREIGN KEY (product_id) REFERENCES dim_product(id),
        FOREIGN KEY(date_id) REFERENCES dim_date(id)
        );         
    -- Trigger function to copy discount from dim_product on insert             
    CREATE OR REPLACE FUNCTION set_discount_from_product()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Get the discount from dim_product and store it in fact_sales
        SELECT discount INTO NEW.discount
        FROM dim_product
        WHERE id = NEW.product_id;
                   
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
        
    -- Create trigger to run before insert
    CREATE OR REPLACE TRIGGER trg_set_discount
        BEFORE INSERT ON fact_sales
        FOR EACH ROW
        EXECUTE FUNCTION set_discount_from_product();

    CREATE OR REPLACE FUNCTION set_price_from_product()
    RETURNS TRIGGER AS $$
    BEGIN
        SELECT price INTO NEW.unit_price
        FROM dim_product
        WHERE id = NEW.product_id;
                
        RETURN NEW;
    END;
    $$LANGUAGE plpgsql;
        
    CREATE OR REPLACE TRIGGER trg_set_price
        BEFORE INSERT ON fact_sales
        FOR EACH ROW
        EXECUTE FUNCTION set_price_from_product();
                        

    

    CREATE TABLE IF NOT EXISTS guest_carts(
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(64) NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        expires_at TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
                 );
    CREATE TABLE IF NOT EXISTS user_carts (
        id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        FOREIGN KEY(product_id) REFERENCES dim_product(id),  
        FOREIGN KEY(customer_id) REFERENCES dim_customers(id)
                      );
    
