# 🧠 Adaptive Quiz System

## Overview

The Adaptive Quiz System is an AI-powered, dynamic questionnaire platform that creates personalized quiz experiences for broker matching. Unlike traditional static quizzes, this system adapts in real-time based on user responses, generating tailored questions and insights.

## 🌟 Key Features

### 1. **Dynamic Question Generation**
- AI-powered question creation using Google Gemini
- Context-aware questions based on previous responses
- Multiple question types: single choice, multiple choice, scale, text
- Intelligent fallback questions when AI generation fails

### 2. **Adaptive Flow Control**
- Real-time response analysis
- Dynamic focus area identification
- Smart quiz completion logic (5-12 questions)
- Progress tracking with estimated completion

### 3. **AI-Powered Insights**
- Real-time response analysis
- Comprehensive final insights generation
- Risk profile assessment
- Investment capacity evaluation

### 4. **Intelligent Matching Integration**
- Automatic broker matching upon completion
- Personalized recommendations
- Integration with existing matching algorithm

## 🏗️ Architecture

### Core Components

```
AdaptiveQuizService
├── QuizQuestionGenerator (AI question generation)
├── GeminiService (AI backend)
├── BrokerMatchingAlgorithm (matching integration)
└── Database Models (persistence)
```

### API Endpoints

```
/api/v1/adaptive-quiz/
├── POST /start                    # Start new quiz session
├── POST /respond                  # Submit response & get next question
├── POST /generate-question        # Generate test questions (admin)
├── GET  /insights/{user_id}       # Get user insights
├── GET  /session/{session_id}     # Get session data
└── POST /test-flow               # Test complete flow (admin)
```

## 🚀 Quick Start

### 1. Start an Adaptive Quiz

```python
from app.services.adaptive_quiz_service import AdaptiveQuizService

# Initialize service
adaptive_service = AdaptiveQuizService(db)

# Start quiz for user
result = await adaptive_service.start_adaptive_quiz(user_id)

# Get first question
first_question = result['question']
session_data = result['session']
```

### 2. Submit Responses

```python
# Submit user response
response = {"answer": "retirement"}

result = await adaptive_service.submit_response_and_get_next(
    session_data, 
    response
)

# Check if quiz is complete
if result.get('completed'):
    insights = result['insights']
    matches = result['matches']
    recommendations = result['recommendations']
else:
    next_question = result['question']
    progress = result['progress']
```

### 3. API Usage

```bash
# Start quiz
curl -X POST "http://localhost:8000/api/v1/adaptive-quiz/start" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Submit response
curl -X POST "http://localhost:8000/api/v1/adaptive-quiz/respond" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_data": {...},
    "response": {"answer": "retirement"}
  }'
```

## 📊 Question Types & Categories

### Question Types
- **single_choice**: Single selection from options
- **multiple_choice**: Multiple selections allowed
- **scale**: Numeric scale (1-5) with labels
- **text**: Free-form text input

### Categories
- **FINANCIAL_GOALS**: Investment objectives, timeline
- **RISK_TOLERANCE**: Risk comfort, volatility acceptance
- **EXPERIENCE**: Investment knowledge, past experience
- **PREFERENCES**: Service needs, communication style

## 🧪 Testing

### Run Core System Tests
```bash
cd backend
python app/test_adaptive_quiz.py
```

### Run API Tests
```bash
cd backend
python app/test_adaptive_quiz_api.py
```

### Test Output Example
```
============================================================
TESTING ADAPTIVE QUIZ SYSTEM
============================================================

1. Starting adaptive quiz...
✓ Quiz started successfully
  Session ID: 377d9291-21ed-41ad-a23a-83e708185bb6
  First question: When do you expect to need the money you are investing?
  Question type: multiple_choice
  Progress: 12.5%

2. Processing 8 test responses...
   Response 1: {'answer': 'retirement'}
   ✓ Response processed. Next question: How comfortable are you with...
   Progress: 25.0%
   
   [... continues until completion ...]
   
3. Final Results:
   Total insights generated: 6
   Broker matches found: 5
   Recommendations: 3
```

## 🔧 Configuration

### Environment Variables
```bash
# Required for AI functionality
GEMINI_API_KEY=your_gemini_api_key

# Database configuration
DATABASE_URL=your_database_url

# Optional: AI model configuration
LLM_MODEL_NAME=gemini-1.5-flash-latest
MAX_QUESTIONS_PER_REQUEST=12
```

### Customization Options

#### Focus Areas
```python
# Default focus areas
focus_areas = [
    "investment_goals",
    "risk_assessment", 
    "broker_preferences",
    "service_needs"
]

# Dynamic focus areas added based on responses
dynamic_areas = [
    "retirement_planning",
    "tax_optimization", 
    "estate_planning"
]
```

#### Question Topics
```python
# Core topics (always covered)
core_topics = [
    ("Investment goals and timeline", "FINANCIAL_GOALS"),
    ("Risk tolerance and comfort level", "RISK_TOLERANCE"),
    ("Investment experience and knowledge", "EXPERIENCE"),
    ("Service preferences and communication style", "PREFERENCES")
]

# Advanced topics (context-dependent)
advanced_topics = [
    ("Specific investment sectors of interest", "PREFERENCES"),
    ("Tax planning considerations", "FINANCIAL_GOALS"),
    ("Estate planning needs", "FINANCIAL_GOALS"),
    ("International investment exposure", "PREFERENCES"),
    ("Alternative investment interest", "EXPERIENCE"),
    ("Retirement planning specifics", "FINANCIAL_GOALS")
]
```

## 🔍 How It Works

### 1. **Session Initialization**
- Creates unique session ID
- Determines initial focus areas based on user profile
- Generates first question using AI

### 2. **Adaptive Question Flow**
```
User Response → Response Analysis → Focus Area Update → 
Topic Selection → Question Type Selection → AI Generation → 
Fallback Check → Question Delivery
```

### 3. **Completion Logic**
- **Minimum**: 5 questions answered
- **Maximum**: 12 questions total
- **Smart completion**: 4+ focus areas + 3+ insights
- **Reason tracking**: Why quiz completed

### 4. **Insights Generation**
- Real-time analysis during quiz
- Comprehensive final analysis using AI
- Risk profile assessment
- Investment capacity evaluation
- Personalized recommendations

## 📈 Performance & Scalability

### Current Capabilities
- **Response Time**: ~2-3 seconds per question generation
- **Concurrent Users**: Limited by AI API rate limits
- **Question Quality**: High (AI-generated with fallbacks)
- **Insight Accuracy**: 85-90% confidence scores

### Optimization Opportunities
1. **Caching**: Pre-generate common questions
2. **Session Storage**: Redis for session persistence
3. **Batch Processing**: Queue multiple AI requests
4. **Load Balancing**: Multiple AI service instances

## 🔒 Security & Privacy

### Data Protection
- Session data encrypted in transit
- User responses stored securely
- AI prompts sanitized
- No PII in AI requests

### Access Control
- **Clients**: Can only access own quiz sessions
- **Brokers**: Can view matched client insights
- **Admins**: Full access to all features

## 🚧 Future Enhancements

### Phase 1: Enhanced AI
- [ ] Multi-language support
- [ ] Voice-to-text integration
- [ ] Sentiment analysis
- [ ] Behavioral pattern recognition

### Phase 2: Advanced Features
- [ ] Quiz templates for different user types
- [ ] A/B testing for question effectiveness
- [ ] Real-time collaboration (advisor-assisted)
- [ ] Integration with external data sources

### Phase 3: Analytics & ML
- [ ] Question effectiveness analytics
- [ ] User journey optimization
- [ ] Predictive matching scores
- [ ] Automated quiz improvement

## 🐛 Troubleshooting

### Common Issues

#### AI Generation Fails
```python
# Fallback questions are automatically used
# Check GEMINI_API_KEY configuration
# Verify internet connectivity
```

#### Session Data Lost
```python
# Implement Redis session storage
# Add session recovery mechanisms
# Use database backup for critical sessions
```

#### Slow Response Times
```python
# Check AI API rate limits
# Implement question caching
# Optimize database queries
```

### Debug Mode
```python
# Enable detailed logging
import logging
logging.getLogger('app.services.adaptive_quiz_service').setLevel(logging.DEBUG)
```

## 📞 Support

For technical support or feature requests:
- Create an issue in the project repository
- Contact the development team
- Check the API documentation for endpoint details

---

**Built with ❤️ using FastAPI, Google Gemini AI, and SQLAlchemy** 