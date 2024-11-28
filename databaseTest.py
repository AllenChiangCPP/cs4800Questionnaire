import mysql.connector
from mysql.connector import Error

#Connection configuration for MySQL database
connection_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'clothingdb'
}

#function for converting image to binary, for later database insertion
def convert_image_to_binary(image_path):
    """Convert an image file to binary data."""
    with open(image_path, 'rb') as file:
        return file.read()

#try to connect to the database
try:
    connection = mysql.connector.connect(**connection_config)
    if connection.is_connected():
        print("Connected to the database.")

    cursor = connection.cursor()

    #query for creating clothing table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS clothing (
        id INT AUTO_INCREMENT PRIMARY KEY,
        img LONGBLOB,  -- Storing binary image data
        colorName VARCHAR(100),
        colorHex VARCHAR(7),
        clothingLocation VARCHAR(100),
        style VARCHAR(255),
        fit VARCHAR(50),
        price_range VARCHAR(50),
        occasion VARCHAR(255),
        patterns VARCHAR(255),
        fabrics VARCHAR(255),
        seasons VARCHAR(50)
    );
    """
    cursor.execute(create_table_query)
    print("Table 'clothing' created successfully.")

    #function for inserting clothing image to database, converts to binary and insert
    def insert_clothing_item(img_path, colorName, colorHex, clothingLocation, style, fit, price_range, occasion, patterns, fabrics, seasons):
        binary_image = convert_image_to_binary(img_path)  #Convert image to binary
        insert_query = """
        INSERT INTO clothing (img, colorName, colorHex, clothingLocation, style, fit, price_range, occasion, patterns, fabrics, seasons)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_tuple = (binary_image, colorName, colorHex, clothingLocation, style, fit, price_range, occasion, patterns, fabrics, seasons)
        cursor.execute(insert_query, data_tuple)
        connection.commit()
        print(f"Inserted a clothing item: {colorName}")

    #insert sample data
    sample_data_list = [
        {
            'img_path': 'clothingImages/image1.jpg',
            'colorName': 'Black',
            'colorHex': '#000000',
            'clothingLocation': 'Outerwear',
            'style': 'Casual',
            'fit': 'Regular',
            'price_range': 'Mid-range ($$)',
            'occasion': 'Casual outings',
            'patterns': 'Solid colors',
            'fabrics': 'Cotton',
            'seasons': 'Fall'
        },
        {
            'img_path': 'clothingImages/image2.jpg',
            'colorName': 'White',
            'colorHex': '#FFFFFF',
            'clothingLocation': 'Top',
            'style': 'Minimalist',
            'fit': 'Slim',
            'price_range': 'Budget ($)',
            'occasion': 'Work',
            'patterns': 'Solid colors',
            'fabrics': 'Linen',
            'seasons': 'Spring'
        },
        {
            'img_path': 'clothingImages/image3.jpg',
            'colorName': 'Navy',
            'colorHex': '#000080',
            'clothingLocation': 'Bottom',
            'style': 'Formal',
            'fit': 'Regular',
            'price_range': 'Premium ($$$)',
            'occasion': 'Formal events',
            'patterns': 'Solid colors',
            'fabrics': 'Wool',
            'seasons': 'Winter'
        },
        {
            'img_path': 'clothingImages/image4.jpg',
            'colorName': 'Beige',
            'colorHex': '#F5F5DC',
            'clothingLocation': 'Top',
            'style': 'Vintage',
            'fit': 'Loose',
            'price_range': 'Mid-range ($$)',
            'occasion': 'Casual outings',
            'patterns': 'Stripes',
            'fabrics': 'Cotton',
            'seasons': 'Spring'
        },
        {
            'img_path': 'clothingImages/image5.jpg',
            'colorName': 'Green',
            'colorHex': '#008000',
            'clothingLocation': 'Bottom',
            'style': 'Athletic',
            'fit': 'Slim',
            'price_range': 'Budget ($)',
            'occasion': 'Sports/Active',
            'patterns': 'Solid colors',
            'fabrics': 'Synthetic',
            'seasons': 'Summer'
        },
        {
            'img_path': 'clothingImages/image6.jpg',
            'colorName': 'Red',
            'colorHex': '#FF0000',
            'clothingLocation': 'Outerwear',
            'style': 'Streetwear',
            'fit': 'Slim',
            'price_range': 'Budget ($)',
            'occasion': 'Evening events',
            'patterns': 'Geometric',
            'fabrics': 'Synthetic',
            'seasons': 'Summer'
        }
    ]

    #Check if data already exists in the table
    cursor.execute("SELECT COUNT(*) FROM clothing")
    count = cursor.fetchone()[0]
    #if table is empty, insert sample data
    if count == 0:
        print("Inserting sample data into the 'clothing' table...")
        for sample_data in sample_data_list:
            insert_clothing_item(
                sample_data['img_path'],
                sample_data['colorName'],
                sample_data['colorHex'],
                sample_data['clothingLocation'],
                sample_data['style'],
                sample_data['fit'],
                sample_data['price_range'],
                sample_data['occasion'],
                sample_data['patterns'],
                sample_data['fabrics'],
                sample_data['seasons']
            )
    else:
        print("Sample data already exists in the 'clothing' table. Skipping insertion.")

    #Fetch and display data from the clothing table to make sure insertion successful
    def fetch_clothing_items():
        select_query = "SELECT id, img, colorName, colorHex, clothingLocation, style, fit, price_range, occasion, patterns, fabrics, seasons FROM clothing"
        cursor.execute(select_query)
        result = cursor.fetchall()
        print("\nData in 'clothing' table:")
        for row in result:
            # Decode the binary image data to verify it's stored correctly (optional)
            id, img, colorName, colorHex, clothingLocation, style, fit, price_range, occasion, patterns, fabrics, seasons = row
            img_preview = img[:10] if img else "No image"
            print(f"ID: {id}, Image (Preview): {img_preview}, Color Name: {colorName}")

    fetch_clothing_items()

except Error as e:
    print("Error:", e)

#close database connection
finally:
    if cursor:
        cursor.close()
    if connection.is_connected():
        connection.close()
    print("Database connection closed.")
