TRANSLATOR_DICTIONARY = {
    "body": {
        "0": "Slim",
        "1": " Average",
        "2": "Athletic",
        "3": " Heavyset"
    },

    "religion": {
        "0": "Not Religious",
        "1": "Spritual, but Not Practicing",
        "2": "Religious",
    },

        "height": {
        "48": "4'",
        "49": "4'1\"",
        "50": "4'2\"",
        "51": "4'3\"",
        "52": "4'4\"",
        "53": "4'5\"",
        "54": "4'6\"",
        "55": "4'7\"",
        "56": "4'8\"",
        "57": "4'9\"",
        "58": "4'10\"",
        "59": "4'11\"",
        "60": "5'",
        "61": "5'1\"",
        "62": "5'2\"",
        "63": "5'3\"",
        "64": "5'4\"",
        "65": "5'5\"",
        "66": "5'6\"",
        "67": "5'7\"",
        "68": "5'8\"",
        "69": "5'9\"",
        "70": "5'10\"",
        "71": "5'11\"",
        "72": "6'",
        "73": "6'1\"",
        "74": "6'2\"",
        "75": "6'3\"",
        "76": "6'4\"",
        "77": "6'5\"",
        "78": "6'6\"",
        "79": "6'7\"",
        "80": "6'8\"",
        "81": "6'9\"",
        "82": "6'10\"",
        "83": "6'11\"",
    },

    "relationship_status": {
        "0": "Never Married",
        "1": "Currently Separated",
        "2": "Divorced",
        "3": "Widowed",
        "4": "Other"
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

