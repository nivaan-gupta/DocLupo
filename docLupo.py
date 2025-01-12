import re

class DoctorChatbot:
    def __init__(self):
        # Database of illnesses and medications by country
        self.medicine_database = {
            "USA": {
                "headache": ["Tylenol", "Advil", "Aleve"],
                "cold": ["DayQuil", "NyQuil", "Sudafed"],
                "heartburn": ["Tums", "Rolaids", "Prilosec OTC"],
                "allergy": ["Claritin", "Zyrtec", "Benadryl"],
                "fever": ["Tylenol", "Advil", "Motrin"],
                "cough": ["Robitussin", "Delsym", "Mucinex"]
            },
            "UK": {
                "headache": ["Paracetamol", "Nurofen", "Anadin"],
                "cold": ["Lemsip", "Sudafed", "Benylin"],
                "heartburn": ["Gaviscon", "Rennie", "Omeprazole"],
                "allergy": ["Piriton", "Clarityn", "Benadryl"],
                "fever": ["Paracetamol", "Ibuprofen", "Aspirin"],
                "cough": ["Covonia", "Benylin", "Buttercup Syrup"]
            },
            "India": {
                "headache": ["Crocin", "Dolo 650", "Saridon"],
                "cold": ["Sinarest", "D-Cold Total", "Vicks Action 500"],
                "heartburn": ["Digene", "Eno", "Pantocid DSR"],
                "allergy": ["Cetirizine", "Allegra", "Avil"],
                "fever": ["Dolo 650", "Paracetamol", "Calpol"],
                "cough": ["Benadryl", "Alex", "Coughsure"]
            },
            "Canada": {
                "headache": ["Tylenol", "Advil", "Aleve"],
                "cold": ["Buckley’s", "NyQuil", "DayQuil"],
                "heartburn": ["Tums", "Zantac", "Rolaids"],
                "allergy": ["Reactine", "Claritin", "Benadryl"],
                "fever": ["Advil", "Tylenol", "Motrin"],
                "cough": ["Buckley’s", "Robitussin", "Delsym"]
            },
            "Australia": {
                "headache": ["Panadol", "Nurofen", "Aspirin"],
                "cold": ["Codral", "Lemsip", "Sudafed"],
                "heartburn": ["Gaviscon", "Rennie", "Mylanta"],
                "allergy": ["Telfast", "Claratyne", "Zyrtec"],
                "fever": ["Panadol", "Nurofen", "Aspirin"],
                "cough": ["Benadryl", "Duro-Tuss", "Dimetapp"]
            },
            "Germany": {
                "headache": ["Aspirin", "Ibuprofen", "Paracetamol"],
                "cold": ["Grippostad", "ACC", "Wick MediNait"],
                "heartburn": ["Talcid", "Maaloxan", "Pantoprazole"],
                "allergy": ["Cetirizine", "Loratadin", "Fenistil"],
                "fever": ["Paracetamol", "Ibuprofen", "Aspirin"],
                "cough": ["Prospan", "Bronchipret", "Mucosolvan"]
            }
        }

    def parse_input(self, user_input):
        # Normalize input and attempt to extract country and illness
        user_input = user_input.lower()

        # Keywords for countries and illnesses
        countries = list(self.medicine_database.keys())
        illnesses = set()
        for country_data in self.medicine_database.values():
            illnesses.update(country_data.keys())

        country = next((country for country in countries if country.lower() in user_input), None)
        illness = next((illness for illness in illnesses if illness in user_input), None)

        return country, illness

    def validate_input(self, user_input):
        """ Validate input and provide context-aware suggestions."""
        if not user_input:
            return "Input cannot be empty. Please describe your issue."
        if len(user_input.split()) < 3:
            return "Your input seems too short. Please include more details about your issue."
        return None

    def suggest_alternatives(self, country, illness):
        """ Suggest alternative illnesses or countries."""
        suggestions = []
        if not country:
            suggestions.append(f"Supported countries: {', '.join(self.medicine_database.keys())}")
        if not illness:
            suggestions.append("Common illnesses include: headache, cold, heartburn, allergy, fever, cough.")
        return suggestions

    def get_medicine(self, country, illness):
        if not country or not illness:
            alternatives = self.suggest_alternatives(country, illness)
            return "\n".join(["Sorry, I couldn't understand your input."] + alternatives)

        country_data = self.medicine_database.get(country.capitalize())
        if not country_data or illness not in country_data:
            alternatives = self.suggest_alternatives(country, illness)
            return "\n".join(["Sorry, I couldn't find a match."] + alternatives)

        medicines = country_data[illness]
        return f"For {illness} in {country.capitalize()}, you can consider these over-the-counter medicines: {', '.join(medicines)}."

if __name__ == "__main__":
    print("Welcome to the DoctorLupo! I can help you find over-the-counter medicines.")
    chatbot = DoctorChatbot()

    while True:
        user_input = input("Describe your issue (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Goodbye! Stay healthy.")
            break

        validation_error = chatbot.validate_input(user_input)
        if validation_error:
            print(validation_error)
            continue

        country, illness = chatbot.parse_input(user_input)
        response = chatbot.get_medicine(country, illness)
        print(response)
        print()
