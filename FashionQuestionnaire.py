import mysql.connector
from mysql.connector import Error
from typing import Dict, List

class FashionQuestionnaire:
    def __init__(self):
        self.questions = {
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

    #function for asking questions to get user response
    def get_responses(self) -> Dict[str, List[str]]:
        """Prompt the user to select options and return their responses."""
        responses = {}
        for question_key, question_data in self.questions.items():
            print(question_data['question'])
            if question_data['type'] == 'multiple':
                print("Select all that apply by entering the numbers separated by spaces.")
            else:
                print("Enter a single number for your choice.")

            for i, option in enumerate(question_data['options'], start=1):
                print(f"{i}. {option}")

            user_input = input("Your selection(s): ").strip()
            selected_indices = [int(x) - 1 for x in user_input.split()]
            responses[question_key] = [question_data['options'][i] for i in selected_indices]
        return responses

    #function for finding best match item based on user's response
    def find_best_match(self, responses: Dict[str, List[str]]):
        connection_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',  
            'database': 'clothingdb'
        }

        #try connecting to database, and use query to select all entries in database table to store in clothing_items dictionary 
        try:
            connection = mysql.connector.connect(**connection_config)
            if connection.is_connected():
                print("Connected to the database.")
            
            cursor = connection.cursor(dictionary=True)

            select_query = """
            SELECT id, img, colorName, colorHex, clothingLocation, style, fit, price_range, occasion, patterns, fabrics, seasons 
            FROM clothing
            """
            cursor.execute(select_query)
            clothing_items = cursor.fetchall()

            #store best match items
            matches = []

            #go through clothing items and score them based on the questionnaire
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

            # Sort matches by score in descending order 
            matches.sort(key=lambda x: x[1], reverse=True)

            # Extract and print top 2 matches
            top_matches = matches[:2]

            if top_matches:
                print("\nTop matches found:")
                for rank, (match, score) in enumerate(top_matches, start=1):
                    print(f"\nRank {rank}:")
                    print("ID:", match['id'])
                    print("Color Name:", match['colorName'])
                    print("Color Hex:", match['colorHex'])
                    print("Clothing Location:", match['clothingLocation'])
                    print("Style:", match['style'])
                    print("Fit:", match['fit'])
                    print("Price Range:", match['price_range'])
                    print("Occasion:", match['occasion'])
                    print("Patterns:", match['patterns'])
                    print("Fabrics:", match['fabrics'])
                    print("Seasons:", match['seasons'])
                    print("Score:", score)
            else:
                print("No matching clothing items found.")
        
        except Error as e:
            print("Error:", e)
        
        #close database connection
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    questionnaire = FashionQuestionnaire()
    user_responses = questionnaire.get_responses()
    questionnaire.find_best_match(user_responses)
