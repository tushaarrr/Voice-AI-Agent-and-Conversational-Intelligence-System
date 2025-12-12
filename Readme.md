# Restaurant Voice AI Agent - Conversational Intelligence System

An intelligent voice-based restaurant assistant built with Twilio Voice API, Flask, and OpenAI GPT-4. This system handles customer inquiries through natural language processing, FAQ matching, and AI-powered fallback responses.

## 🎯 Project Overview

This is a **production-ready voice AI agent** that enables restaurants to automate customer service calls. The system intelligently routes queries through:
- **Local FAQ matching** for common questions
- **OpenAI GPT-4 fallback** for complex queries
- **Human agent transfer** when needed
- **Multi-turn conversations** with context awareness

## 🚀 Features

- **Voice-to-Text Processing**: Real-time speech recognition via Twilio
- **Intelligent FAQ Matching**: Keyword-based matching for common restaurant queries
- **AI-Powered Fallback**: OpenAI GPT-4o-mini integration for natural language understanding
- **Agent Transfer**: Seamless handoff to human support when requested
- **Multi-turn Conversations**: Maintains context across conversation turns
- **Follow-up Prompts**: Proactive suggestions for reservations, specials, and orders
- **Hindi Greeting Integration**: Cultural localization with "Dhanyavaad" in responses

## 📊 Data Science Aspects

This project can be treated as a **Data Science project** because it involves:

### 1. **Natural Language Processing (NLP)**
   - Speech-to-text conversion
   - Intent classification and keyword matching
   - Text similarity analysis for FAQ matching

### 2. **Conversational AI**
   - Multi-turn dialogue management
   - Context preservation across interactions
   - Response generation using LLMs (GPT-4o-mini)

### 3. **Machine Learning Integration**
   - OpenAI GPT-4o-mini for intelligent fallback responses
   - Confidence scoring from speech recognition
   - Adaptive response generation based on user queries

### 4. **Data Collection & Analysis**
   - Call logs and conversation transcripts
   - User query patterns and intent analysis
   - Performance metrics (response time, accuracy)
   - FAQ effectiveness measurement

### 5. **Potential ML Enhancements**
   - Intent classification models
   - Sentiment analysis for customer satisfaction
   - Query clustering for FAQ optimization
   - Predictive analytics for common questions

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask
- **Voice API**: Twilio Voice API with Speech Recognition
- **AI/ML**: OpenAI GPT-4o-mini API
- **Environment**: python-dotenv
- **HTTP Client**: requests
- **Deployment**: ngrok (development), production-ready for cloud deployment

## 📋 Prerequisites

- Python 3.9 or later
- Twilio account with Voice-enabled phone number
- OpenAI API key
- ngrok (for local development)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tushaarrr/Voice-AI-Agent-and-Conversational-Intelligence-System.git
cd Voice-AI-Agent-and-Conversational-Intelligence-System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
OPENAI_API_KEY=your_openai_api_key
SUPPORT_NUMBER=+1234567890
PORT=5050
```

## 🚀 Quick Start

### 1. Start the Flask Server

```bash
python answer_phone.py
```

The server will start on `http://0.0.0.0:5050`

### 2. Expose with ngrok

In a new terminal:

```bash
ngrok http 5050
```

Copy the ngrok URL (e.g., `https://abc123.ngrok-free.app`)

### 3. Configure Twilio Webhook

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Phone Numbers** → **Manage** → **Active Numbers**
3. Click your phone number
4. In **Voice Configuration**, set:
   - **A call comes in**: Webhook
   - **URL**: `https://your-ngrok-url.ngrok-free.app/`
   - **HTTP Method**: POST
5. Save configuration

### 4. Test the System

Call your Twilio phone number and interact with the voice bot!

## 📡 API Endpoints

### `POST /`
Handles incoming calls and returns initial TwiML response.

**Response**: TwiML with welcome message and speech gathering

### `POST /voice`
Processes user speech input and returns appropriate response.

**Request Parameters**:
- `SpeechResult`: Transcribed user speech
- `Confidence`: Speech recognition confidence score

**Response Types**:
- FAQ match → Returns FAQ answer
- Agent request → Transfers to support number
- No match → OpenAI fallback response

## 🎤 Supported FAQ Topics

The bot can answer questions about:
- **Hours**: Restaurant operating hours
- **Address**: Location and directions
- **Vegan**: Vegan menu options
- **Reservation**: Booking information
- **Delivery**: Delivery services and partners
- **Parking**: Parking availability and options
- **Payment**: Accepted payment methods
- **Kids**: Family-friendly amenities

## 📝 Example Conversations

### FAQ Match
**User**: "What are your hours?"
**Bot**: "We're open Monday through Thursday from 11 AM to 10 PM..."

### AI Fallback
**User**: "What's your chef's favorite dish?"
**Bot**: "[AI-generated response] Dhanyavaad!"

### Agent Transfer
**User**: "I want to talk to an agent"
**Bot**: "Connecting you to a human" → Transfers call

## 🧪 Testing

### Test with curl

```bash
# Test root endpoint
curl -X POST https://your-ngrok-url.ngrok-free.app/ \
  -d "From=+1234567890&To=+15796003576&CallSid=test123"

# Test voice endpoint with FAQ
curl -X POST https://your-ngrok-url.ngrok-free.app/voice \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "SpeechResult=Do you have parking?"

# Test OpenAI fallback
curl -X POST https://your-ngrok-url.ngrok-free.app/voice \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "SpeechResult=What's your chef's favorite dish?"
```

Or use the provided test script:

```bash
chmod +x curl_example.sh
./curl_example.sh
```

## 📊 Data Science Use Cases

### 1. **Conversation Analytics**
- Analyze call transcripts for common patterns
- Identify frequently asked questions
- Measure response accuracy and user satisfaction

### 2. **Intent Classification**
- Build ML models to classify user intents
- Improve FAQ matching accuracy
- Reduce false positives in keyword matching

### 3. **Sentiment Analysis**
- Analyze customer sentiment from conversations
- Identify frustrated customers for priority handling
- Track satisfaction trends over time

### 4. **Query Optimization**
- Cluster similar queries to optimize FAQ responses
- Identify gaps in FAQ coverage
- Generate new FAQ entries from common queries

### 5. **Predictive Analytics**
- Predict peak inquiry times
- Forecast common question patterns
- Optimize agent transfer thresholds

## 🔒 Security Notes

- Never commit `.env` file to version control
- Keep API keys secure and rotate regularly
- Use environment variables for sensitive data
- Implement rate limiting for production

## 📁 Project Structure

```
.
├── answer_phone.py          # Main Flask application
├── app.py                   # Alternative FastAPI implementation
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── curl_example.sh         # Testing script
├── README.md               # This file
└── LICENSE                 # License file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Twilio](https://www.twilio.com/) for Voice API
- [OpenAI](https://openai.com/) for GPT-4 API
- [Flask](https://flask.palletsprojects.com/) framework

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Note**: This project demonstrates production-ready voice AI integration with intelligent fallback mechanisms and can serve as a foundation for advanced conversational AI systems.
