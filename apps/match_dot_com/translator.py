TRANSLATOR_DICTIONARY = {
    "body": {
        "0": "Slim",
        "1": " Average",
        "2": "Athletic",
        "3": " Heavyset"
    },

    "relationship_status": {
        "0": "Never",
        "1": "Possibly",
        "2": "Someday"
    },

    "current_kids": {
        "0": "No",
        "3": "Yes, and they live with me",
        "2": "Yes, and they sometimes live with me",
        "1": "Yes, but they do not live with me"
    },


    "future_kids": {
        "5": "Definitely",
        "4": "Someday",
        "2": "Not Sure",
        "1": "Probably Not",
        "0": "No",
        "3": "No, but it's okay if my partner does."
    },

    "education": {
        "0": "No Highschool",
        "1": "High School",
        "2": "Some College",
        "3": "College Graduate",
        "4": "Graduate School",
        "5": "Doctorate" 
    },

    "drink": {
        "0": "Never",
        "1": "Social Drinker",
        "2": "Moderately",
        "3": "Regularly"
    },

    "smoke": {
        "0": "No",
        "1": "Trying to quit",
        "2": "Occasionally",
        "3": "Daily",
        "4": "Like a chimney"
    },

    "salary": {
        "0": "Struggling",
        "1": "Comfortable",
        "2": "Affluent"
    }
}

def translate(key, index):
    return TRANSLATOR_DICTIONARY[key][str(index)]

