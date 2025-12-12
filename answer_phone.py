from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Say, Gather, Dial
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
SUPPORT_NUMBER = os.getenv('SUPPORT_NUMBER', '+919711840175')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Restaurant FAQ
FAQ = {
    "hours": "We're open Monday through Thursday from 11 AM to 10 PM, Friday and Saturday from 11 AM to 11 PM, and Sunday from 12 PM to 9 PM.",
    "address": "We're located at 123 Main Street, Downtown District. We're right next to the Central Park, you can't miss us!",
    "vegan": "Yes, we have a dedicated vegan menu with over 15 delicious options including our famous vegan burger, quinoa bowls, and dairy-free desserts.",
    "reservation": "You can make reservations by calling us directly, booking online through our website, or using OpenTable. We recommend booking at least 24 hours in advance for weekend dining.",
    "delivery": "We offer delivery through DoorDash, Uber Eats, and Grubhub. Delivery is available within a 5-mile radius and typically takes 30-45 minutes.",
    "parking": "We have a complimentary valet parking service, and there's also a public parking garage two blocks away with reasonable rates.",
    "payment": "We accept all major credit cards, Apple Pay, Google Pay, and cash. We also accept contactless payments for your convenience.",
    "kids": "Absolutely! We're very family-friendly with a dedicated kids menu, high chairs, and booster seats available. Kids under 5 eat free on weekdays!"
}

def find_faq_match(user_text):
    """Find matching FAQ entry based on user input."""
    if not user_text:
        return None
        
    user_text_lower = user_text.lower()
    print(f"Processing user input: '{user_text}'")
    
    # Check for agent keyword first
    if "agent" in user_text_lower:
        print("Agent keyword detected")
        return "agent"
    
    # Handle specials and ordering intents explicitly
    if "special" in user_text_lower:
        print("Specials keyword detected")
        return (
            "Today's specials are: Chef's butter chicken with basmati rice, grilled paneer tikka, "
            "and mango lassi. Would you like to hear more or place an order?"
        )
    if "order" in user_text_lower or "takeout" in user_text_lower or "pickup" in user_text_lower:
        print("Order intent detected")
        return (
            "Great, I can help start a takeout order. Please say the items you want, or say agent "
            "to talk to a human."
        )
    
    # Check for FAQ keyword matches
    for keyword, answer in FAQ.items():
        if keyword in user_text_lower:
            print(f"Found FAQ match for keyword: '{keyword}'")
            return answer
    
    print("No FAQ match found")
    return None

def get_openai_fallback_reply(user_text: str) -> str:
    """Call OpenAI Chat Completions API to get a polite fallback. Returns plain text."""
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY not set. Skipping OpenAI fallback.")
        return "I am sorry, I did not catch that. Please try again. Dhanyavaad!"

    try:
        print("Calling OpenAI for fallback reply")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        system_prompt = (
            "You are a friendly restaurant voice assistant. Keep responses short, clear, and helpful. "
            "Answer based on common restaurant context like hours, address, menu highlights, reservations, delivery, parking, payment, and kids options."
        )
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.5,
            "max_tokens": 120
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        if resp.status_code != 200:
            print(f"OpenAI API error: {resp.status_code} {resp.text}")
            return "I am sorry, I did not catch that. Please try again. Dhanyavaad!"
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        content = (content or "I am sorry, I did not catch that.").strip()
        return f"{content} Dhanyavaad!"
    except Exception as e:
        print(f"Exception calling OpenAI: {e}")
        return "I am sorry, I did not catch that. Please try again. Dhanyavaad!"

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with restaurant voice bot."""
    print("Handling incoming call")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request data: {request.form.to_dict()}")
    
    resp = VoiceResponse()
    resp.say("Welcome to our restaurant! How can I help you today?")
    
    gather = Gather(action="/voice", method="POST", input="speech", speech_timeout=3)
    gather.say("Please speak your question after the beep.")
    resp.append(gather)
    
    # Fallback if no input
    resp.say("I didn't hear anything. Please call back and try again.")
    
    print(f"Returning TwiML: {str(resp)}")
    return str(resp), 200, {'Content-Type': 'application/xml'}

@app.route("/voice", methods=['GET', 'POST'])
def handle_voice():
    """Handle voice input and respond with FAQ or agent transfer."""
    print("Received voice input")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request data: {request.form.to_dict()}")
    
    # Get the speech result from Twilio
    speech_result = request.values.get('SpeechResult', '')
    print(f"Speech result: '{speech_result}'")
    
    # Find FAQ match
    faq_response = find_faq_match(speech_result)
    
    resp = VoiceResponse()
    
    if faq_response == "agent":
        print("Handling agent request")
        resp.say("Connecting you to a human")
        if SUPPORT_NUMBER:
            resp.dial(SUPPORT_NUMBER)
        else:
            resp.say("Sorry, no support number is configured")
    elif faq_response:
        print(f"Responding with FAQ: {faq_response}")
        gather = Gather(action="/voice", method="POST", input="speech", speech_timeout=3)
        gather.say(faq_response)
        # Follow-up prompt to drive next action
        gather.say("Would you like to make a reservation, hear today's specials, or place an order?")
        resp.append(gather)
    else:
        print("No match found, using OpenAI fallback")
        fallback_text = get_openai_fallback_reply(speech_result)
        gather = Gather(action="/voice", method="POST", input="speech", speech_timeout=3)
        gather.say(fallback_text)
        resp.append(gather)
    
    print(f"Returning TwiML: {str(resp)}")
    return str(resp), 200, {'Content-Type': 'application/xml'}

if __name__ == "__main__":
    print("Starting Restaurant Voice Bot on port 5050")
    app.run(host="0.0.0.0", port=5050, debug=False, use_reloader=False)
