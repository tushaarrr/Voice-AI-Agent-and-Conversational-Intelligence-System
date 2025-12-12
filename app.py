import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from twilio.twiml.voice_response import VoiceResponse, Say, Gather, Dial
from dotenv import load_dotenv

load_dotenv()

# Configuration
SUPPORT_NUMBER = os.getenv('SUPPORT_NUMBER')
PORT = int(os.getenv('PORT', 5050))

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

app = FastAPI()

def find_faq_match(user_text):
    """Find matching FAQ entry based on user input."""
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

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Restaurant Voice Bot is running!"}

@app.post("/voice")
async def handle_voice_request(request: Request):
    """Handle voice requests with SpeechResult."""
    try:
        print("Received POST request to /voice")
        print(f"Content-Type: {request.headers.get('content-type')}")
        
        # Parse request data - handle both JSON and form data
        data = {}
        content_type = request.headers.get("content-type", "")
        
        if "application/json" in content_type:
            try:
                data = await request.json()
                print("Parsed as JSON")
            except Exception as json_error:
                print(f"JSON parsing failed: {json_error}")
                # Fallback to form data
                form_data = await request.form()
                data = dict(form_data)
                print("Fell back to form data")
        else:
            # Handle form data
            form_data = await request.form()
            data = dict(form_data)
            print("Parsed as form data")
        
        print(f"Request data: {data}")
        
        speech_result = data.get("SpeechResult", "")
        if not speech_result:
            print("No SpeechResult found in request")
            speech_result = ""
        
        # Find FAQ match
        faq_response = find_faq_match(speech_result)
        
        # Create TwiML response
        response = VoiceResponse()
        
        if faq_response == "agent":
            print("Handling agent request")
            response.say("Connecting you to a human")
            if SUPPORT_NUMBER:
                response.dial(SUPPORT_NUMBER)
            else:
                response.say("Sorry, no support number is configured")
        elif faq_response:
            print(f"Responding with FAQ/intent: {faq_response}")
            gather = Gather(action="/voice", method="POST")
            gather.say(faq_response)
            # Follow-up prompt to drive next action
            gather.say("Would you like to make a reservation, hear today's specials, or place an order?")
            response.append(gather)
        else:
            print("No match found, asking for repetition")
            gather = Gather(action="/voice", method="POST")
            gather.say("Sorry, could you repeat that? Or say agent to talk to a human.")
            response.append(gather)
        
        twiml = str(response)
        print(f"Returning TwiML: {twiml}")
        
        return HTMLResponse(content=twiml, media_type="application/xml")
        
    except Exception as e:
        print(f"Error processing voice request: {str(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        response = VoiceResponse()
        response.say("Sorry, there was an error processing your request. Please try again.")
        return HTMLResponse(content=str(response), media_type="application/xml")

@app.api_route("/voice", methods=["GET", "PUT", "DELETE", "PATCH"])
async def voice_method_not_allowed():
    """Return 405 for non-POST methods to /voice."""
    raise HTTPException(status_code=405, detail="Method not allowed. Only POST is supported.")

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response."""
    try:
        print("Handling incoming call")
        response = VoiceResponse()
        response.say("Welcome to our restaurant! How can I help you today?")
        
        gather = Gather(action="/voice", method="POST")
        gather.say("Please speak your question after the beep.")
        response.append(gather)
        
        # Fallback if no input
        response.say("I didn't hear anything. Please call back and try again.")
        
        twiml = str(response)
        print(f"Returning incoming call TwiML: {twiml}")
        
        return HTMLResponse(content=twiml, media_type="application/xml")
        
    except Exception as e:
        print(f"Error handling incoming call: {str(e)}")
        response = VoiceResponse()
        response.say("Sorry, there was an error. Please try again later.")
        return HTMLResponse(content=str(response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    print(f"Starting Restaurant Voice Bot on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)