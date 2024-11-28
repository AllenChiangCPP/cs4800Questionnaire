from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use Flask sessions

#function for fetching clothes from database
def fetch_clothing_items():
    #configure database connection
    """Fetch clothing items from the database."""
    connection_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '', 
        'database': 'clothingdb'
    }
    #try to select database item 
    try:
        connection = mysql.connector.connect(**connection_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            select_query = """
            SELECT id, img, colorName, colorHex, clothingLocation, style, fit, price_range, occasion, patterns, fabrics, seasons 
            FROM clothing
            """
            cursor.execute(select_query)
            clothing_items = cursor.fetchall()
            #Convert binary image data to base64
            for item in clothing_items:
                if item['img']:
                    item['img'] = base64.b64encode(item['img']).decode('utf-8')
            return clothing_items
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

#funciton for getting best match clothing items based on user response
def calculate_matches(responses, clothing_items):
    """Calculate match scores for clothing items based on user responses."""
    #go through clothing_items, total score for each item and add to matches array
    matches = []
    for item in clothing_items:
        score = 0
        if item['colorName'] in responses.get('colors', []):
            score += 1
        if item['style'] in responses.get('styles', []):
            score += 1
        if item['fit'] in responses.get('fit', []):
            score += 1
        if item['price_range'] in responses.get('price_range', []):
            score += 1
        if item['occasion'] in responses.get('occasions', []):
            score += 1
        if item['patterns'] in responses.get('patterns', []):
            score += 1
        if item['fabrics'] in responses.get('fabrics', []):
            score += 1
        if item['seasons'] in responses.get('seasons', []):
            score += 1
        matches.append((item, score))
    #sort array by best match and return top 3 results
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:3]  

#function for converting image to binary
def convert_image_to_binary(image_path):
    """Convert an image file to binary data."""
    with open(image_path, 'rb') as file:
        return file.read()

#displays main page and set of questions
@app.route('/')
def index():
    questions = {
        'colors': {
            'question': 'Which colors do you prefer in your wardrobe? (Select all that apply)',
            'options': ['Black', 'White', 'Navy', 'Beige', 'Gray', 'Brown', 'Red', 'Green', 'Blue', 'Purple', 'Pink'],
            'type': 'multiple'
        },
        'styles': {
            'question': 'Which fashion styles resonate with you? (Select all that apply)',
            'options': ['Casual', 'Formal', 'Streetwear', 'Minimalist', 'Vintage', 'Athletic'],
            'type': 'multiple'
        },
        'fit': {
            'question': 'What type of fit do you prefer?',
            'options': ['Loose', 'Regular', 'Slim'],
            'type': 'multiple'
        },
        'price_range': {
            'question': 'What is your preferred price range for clothing items?',
            'options': ['Budget ($)', 'Mid-range ($$)', 'Premium ($$$)', 'Luxury ($$$$)'],
            'type': 'single'
        },
        'occasions': {
            'question': 'What occasions do you typically dress for?',
            'options': ['Work', 'Casual outings', 'Formal events', 'Sports/Active', 'Evening events'],
            'type': 'multiple'
        },
        'patterns': {
            'question': 'Which patterns do you prefer?',
            'options': ['Solid colors', 'Stripes', 'Floral', 'Geometric', 'Animal print', 'Plaid'],
            'type': 'multiple'
        },
        'fabrics': {
            'question': 'Which fabric types do you prefer?',
            'options': ['Cotton', 'Linen', 'Silk', 'Wool', 'Denim', 'Synthetic'],
            'type': 'multiple'
        },
        'seasons': {
            'question': 'Which seasons are you shopping for?',
            'options': ['Spring', 'Summer', 'Fall', 'Winter'],
            'type': 'multiple'
        }
    }

    return render_template('index.html', questions=questions)

#function for handling form submission, collect and stores responses
@app.route('/submit', methods=['POST'])
def submit():
    # Get the submitted responses
    responses = request.form.to_dict(flat=False)  # Collect multiple values for checkboxes
    session['responses'] = responses  # Save the responses in the session
    return redirect(url_for('results'))

#function for displayinh results, passes top 3 matches to results.html for display
@app.route('/results')
def results():
    responses = session.get('responses', {})
    clothing_items = fetch_clothing_items()
    top_matches = calculate_matches(responses, clothing_items)
    return render_template('results.html', matches=top_matches)

if __name__ == "__main__":
    app.run(debug=True)
