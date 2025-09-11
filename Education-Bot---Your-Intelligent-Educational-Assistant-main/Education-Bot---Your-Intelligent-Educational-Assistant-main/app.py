from flask import Flask, request, jsonify, render_template, session
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import logging
import re
import random
import uuid
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import ssl

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize NLTK
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    logger.warning("Some NLTK data downloads failed, continuing with basic functionality")

# Initialize NLTK components
try:
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
except:
    lemmatizer = None
    stop_words = set()

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  # For session management

# Get Google Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize the Gemini client
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    logger.error("Google Gemini API key is not set! Make sure you have a .env file with GEMINI_API_KEY")
    client = None

# Store conversation history in memory only (will be cleared on server restart)
conversation_history = {}

# Education-focused topics 
EDUCATIONAL_DOMAINS = [
    "mathematics", "algebra", "geometry", "calculus", "statistics", "probability",
    "physics", "chemistry", "biology", "anatomy", "astronomy", "earth science",
    "history", "geography", "civics", "economics", "political science",
    "literature", "grammar", "writing", "poetry", "language arts",
    "computer science", "programming", "data science", "artificial intelligence",
    "art history", "music theory", "philosophy", "psychology", "sociology",
    "foreign languages", "education", "study skills", "research methods"
]

def analyze_user_input(text):
    """Analyze user input using NLTK for better understanding."""
    try:
        if not lemmatizer or not stop_words:
            return {"tokens": [], "key_concepts": [], "question_type": "general", "complexity": "medium"}
        
        # Tokenize and clean
        tokens = word_tokenize(text.lower())
        
        # Remove stop words and punctuation
        meaningful_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
        
        # Lemmatize
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in meaningful_tokens]
        
        # POS tagging to identify key concepts (nouns, adjectives)
        pos_tags = pos_tag(meaningful_tokens)
        key_concepts = [word for word, pos in pos_tags if pos.startswith('NN') or pos.startswith('JJ')]
        
        # Determine question type
        question_type = "general"
        if any(word in text.lower() for word in ["what", "define", "explain"]):
            question_type = "definition"
        elif any(word in text.lower() for word in ["how", "solve", "calculate"]):
            question_type = "procedural"
        elif any(word in text.lower() for word in ["why", "because", "reason"]):
            question_type = "conceptual"
        elif any(word in text.lower() for word in ["compare", "difference", "similar"]):
            question_type = "comparison"
        
        # Estimate complexity based on vocabulary and sentence structure
        sentences = sent_tokenize(text)
        avg_sentence_length = sum(len(word_tokenize(sentence)) for sentence in sentences) / len(sentences)
        
        complexity = "medium"
        if avg_sentence_length > 15 or len(key_concepts) > 5:
            complexity = "high"
        elif avg_sentence_length < 8 and len(key_concepts) < 3:
            complexity = "low"
        
        return {
            "tokens": lemmatized_tokens,
            "key_concepts": key_concepts,
            "question_type": question_type,
            "complexity": complexity,
            "sentence_count": len(sentences),
            "word_count": len(meaningful_tokens)
        }
    
    except Exception as e:
        logger.warning(f"NLTK analysis failed: {e}")
        return {"tokens": [], "key_concepts": [], "question_type": "general", "complexity": "medium"}

def enhance_educational_prompt(user_input, analysis):
    """Enhance the educational prompt based on NLTK analysis."""
    base_prompt = f"User question: {user_input}\\n\\n"
    
    # Add context based on analysis
    if analysis["question_type"] == "definition":
        base_prompt += "This appears to be a definition question. Please provide a clear, comprehensive explanation with examples.\\n"
    elif analysis["question_type"] == "procedural":
        base_prompt += "This appears to be a procedural question. Please provide step-by-step instructions or methods.\\n"
    elif analysis["question_type"] == "conceptual":
        base_prompt += "This appears to be a conceptual question. Please explain the underlying principles and reasoning.\\n"
    elif analysis["question_type"] == "comparison":
        base_prompt += "This appears to be a comparison question. Please highlight similarities and differences clearly.\\n"
    
    # Add complexity guidance
    if analysis["complexity"] == "high":
        base_prompt += "This is a complex question. Please break down the answer into manageable parts and use clear explanations.\\n"
    elif analysis["complexity"] == "low":
        base_prompt += "This is a straightforward question. Please provide a concise but complete answer.\\n"
    
    # Add key concepts if found
    if analysis["key_concepts"]:
        key_concepts_str = ", ".join(analysis["key_concepts"][:5])  # Limit to top 5
        base_prompt += f"Key concepts identified: {key_concepts_str}. Please make sure to address these in your response.\\n"
    
    return base_prompt

@app.route('/')
def home():
    # Create a unique session ID if not exists - but don't persist history
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        # Initialize an empty conversation history for this session
        conversation_history[session['session_id']] = []
    
    # Return the modern dark-themed HTML directly from Python
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduBot Pro - AI Educational Assistant</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #1a1a1a;
            --bg-tertiary: #2a2a2a;
            --bg-chat: #1e1e1e;
            --text-primary: #ffffff;
            --text-secondary: #b4b4b4;
            --text-accent: #03a9f4;
            --border-color: #333333;
            --accent-primary: #03a9f4;
            --accent-secondary: #9c27b0;
            --accent-gold: #ffc107;
            --success: #4caf50;
            --warning: #ff9800;
            --error: #f44336;
            --shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            --gradient: linear-gradient(135deg, #03a9f4 0%, #9c27b0 50%, #ffc107 100%);
            --glow-blue: rgba(3, 169, 244, 0.3);
            --glow-purple: rgba(156, 39, 176, 0.3);
            --glow-gold: rgba(255, 193, 7, 0.3);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .main-container {
            display: flex;
            height: 100vh;
            background: var(--bg-primary);
        }

        .sidebar {
            width: 280px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            transition: all 0.3s ease;
        }

        .sidebar-header {
            padding: 24px;
            border-bottom: 1px solid var(--border-color);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
        }

        .logo-icon {
            width: 32px;
            height: 32px;
            background: var(--gradient);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }

        .new-chat-btn {
            width: 100%;
            padding: 12px 16px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .new-chat-btn:hover {
            background: var(--bg-chat);
            border-color: var(--accent-primary);
            box-shadow: 0 0 15px var(--glow-blue);
            transform: translateY(-2px);
        }

        .sidebar-content {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
        }

        .quick-actions {
            margin-bottom: 24px;
        }

        .quick-actions h3 {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .action-item {
            padding: 12px 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 4px;
            font-size: 14px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .action-item:hover {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .action-icon {
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-primary);
        }

        .chat-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-color);
            background: var(--bg-secondary);
        }

        .chat-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .chat-subtitle {
            font-size: 14px;
            color: var(--text-secondary);
        }

        .chat-messages {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
            scroll-behavior: smooth;
        }

        .message {
            margin-bottom: 24px;
            animation: slideUp 0.3s ease;
        }

        .message-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }

        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 600;
        }

        .user-avatar {
            background: var(--accent-primary);
            color: var(--bg-primary);
        }

        .bot-avatar {
            background: var(--gradient);
            color: white;
        }

        .message-sender {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .message-time {
            font-size: 12px;
            color: var(--text-secondary);
            margin-left: auto;
        }

        .message-content {
            margin-left: 44px;
            line-height: 1.6;
            color: var(--text-primary);
        }

        .message-content p {
            margin-bottom: 12px;
        }

        .message-content:last-child {
            margin-bottom: 0;
        }

        .message-content code {
            background: var(--bg-tertiary);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
            color: var(--accent-primary);
        }

        .message-content pre {
            background: var(--bg-tertiary);
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 12px 0;
            border: 1px solid var(--border-color);
        }

        .message-content pre code {
            background: none;
            padding: 0;
            color: var(--text-primary);
        }

        .typing-indicator {
            margin-left: 44px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 0;
        }

        .typing-dots {
            display: flex;
            gap: 4px;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-primary);
            border-radius: 50%;
            animation: typingGlow 1.4s infinite ease-in-out;
        }

        .typing-dot:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-dot:nth-child(3) {
            animation-delay: 0.4s;
        }

        .input-area {
            padding: 24px;
            border-top: 1px solid var(--border-color);
            background: var(--bg-secondary);
        }

        .input-container {
            position: relative;
            max-width: 800px;
            margin: 0 auto;
        }

        .input-field {
            width: 100%;
            min-height: 56px;
            padding: 16px 60px 16px 20px;
            background: var(--bg-primary);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 16px;
            font-family: inherit;
            resize: none;
            outline: none;
            transition: all 0.2s ease;
            line-height: 1.4;
        }

        .input-field:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px var(--glow-blue), 0 0 20px var(--glow-blue);
            transform: translateY(-2px);
        }

        .input-field::placeholder {
            color: var(--text-secondary);
        }

        .send-button {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            width: 40px;
            height: 40px;
            background: var(--gradient);
            border: 2px solid var(--accent-gold);
            border-radius: 8px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            box-shadow: 0 4px 15px var(--glow-blue);
        }

        .send-button:hover {
            background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-secondary) 100%);
            transform: translateY(-50%) scale(1.1);
            box-shadow: 0 8px 25px var(--glow-gold), 0 0 30px var(--glow-purple);
        }

        .send-button:disabled {
            background: var(--text-secondary);
            cursor: not-allowed;
            transform: translateY(-50%) scale(1);
        }

        .suggestion-chips {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }

        .suggestion-chip {
            padding: 8px 16px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            font-size: 14px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .suggestion-chip:hover {
            background: var(--accent-primary);
            color: var(--bg-primary);
            border-color: var(--accent-primary);
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes pulse {
            0%, 80%, 100% {
                transform: scale(0);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }

        @keyframes typingGlow {
            0%, 80%, 100% {
                transform: scale(0.8);
                opacity: 0.4;
                box-shadow: 0 0 5px var(--glow-blue);
            }
            40% {
                transform: scale(1.2);
                opacity: 1;
                box-shadow: 0 0 15px var(--glow-blue), 0 0 25px var(--glow-purple);
            }
        }

        .welcome-screen {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            text-align: center;
            max-width: 600px;
            margin: 0 auto;
            padding: 40px;
        }

        .welcome-icon {
            width: 80px;
            height: 80px;
            background: var(--gradient);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin-bottom: 24px;
        }

        .welcome-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .welcome-subtitle {
            font-size: 18px;
            color: var(--text-secondary);
            margin-bottom: 32px;
            line-height: 1.5;
        }

        .welcome-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            width: 100%;
            margin-bottom: 32px;
        }

        .feature-card {
            padding: 20px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            text-align: left;
        }

        .feature-icon {
            font-size: 24px;
            margin-bottom: 12px;
            color: var(--accent-primary);
        }

        .feature-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .feature-desc {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        @media (max-width: 768px) {
            .sidebar {
                display: none;
            }
            
            .chat-messages {
                padding: 16px;
            }
            
            .input-area {
                padding: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="sidebar">
            <div class="sidebar-header">
                <div class="logo">
                    <div class="logo-icon">🎓</div>
                    <span>EduBot Pro</span>
                </div>
                <button class="new-chat-btn" onclick="clearChat()">
                    <span>➕</span>
                    <span>New Chat</span>
                </button>
            </div>
            <div class="sidebar-content">
                <div class="quick-actions">
                    <h3>Quick Topics</h3>
                    <div class="action-item" onclick="suggestTopic('mathematics')">
                        <div class="action-icon">📊</div>
                        <span>Mathematics</span>
                    </div>
                    <div class="action-item" onclick="suggestTopic('science')">
                        <div class="action-icon">🔬</div>
                        <span>Science</span>
                    </div>
                    <div class="action-item" onclick="suggestTopic('programming')">
                        <div class="action-icon">💻</div>
                        <span>Programming</span>
                    </div>
                    <div class="action-item" onclick="suggestTopic('history')">
                        <div class="action-icon">🏛️</div>
                        <span>History</span>
                    </div>
                    <div class="action-item" onclick="suggestTopic('literature')">
                        <div class="action-icon">📚</div>
                        <span>Literature</span>
                    </div>
                    <div class="action-item" onclick="suggestTopic('physics')">
                        <div class="action-icon">⚛️</div>
                        <span>Physics</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <div class="chat-title">Educational AI Assistant</div>
                <div class="chat-subtitle">Ask me anything about learning and education</div>
            </div>

            <div class="chat-messages" id="chat-messages">
                <div class="welcome-screen" id="welcome-screen">
                    <div class="welcome-icon">🎓</div>
                    <h1 class="welcome-title">Welcome to EduBot Pro</h1>
                    <p class="welcome-subtitle">Your intelligent educational assistant powered by advanced AI. Ask me anything about learning, get help with homework, or explore new topics!</p>
                    
                    <div class="welcome-features">
                        <div class="feature-card">
                            <div class="feature-icon">🧮</div>
                            <div class="feature-title">Mathematics</div>
                            <div class="feature-desc">Solve problems, learn concepts, and understand formulas</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🔬</div>
                            <div class="feature-title">Science</div>
                            <div class="feature-desc">Explore physics, chemistry, biology, and more</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">📖</div>
                            <div class="feature-title">Literature</div>
                            <div class="feature-desc">Analyze texts, understand themes, and improve writing</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🌍</div>
                            <div class="feature-title">History</div>
                            <div class="feature-desc">Learn about events, cultures, and civilizations</div>
                        </div>
                    </div>

                    <div class="suggestion-chips">
                        <div class="suggestion-chip" onclick="sendMessage('Explain quantum physics in simple terms')">Explain quantum physics</div>
                        <div class="suggestion-chip" onclick="sendMessage('Help me solve calculus problems')">Calculus help</div>
                        <div class="suggestion-chip" onclick="sendMessage('Teach me about World War II')">World War II</div>
                        <div class="suggestion-chip" onclick="sendMessage('Programming fundamentals')">Programming basics</div>
                    </div>
                </div>
            </div>

            <div class="input-area">
                <div class="input-container">
                    <textarea 
                        id="message-input" 
                        class="input-field" 
                        placeholder="Ask me anything about education..." 
                        rows="1"
                        onkeydown="handleKeyPress(event)"
                    ></textarea>
                    <button id="send-button" class="send-button" onclick="sendMessage()">
                        <span>➤</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isTyping = false;

        function formatMessage(text) {
            // Basic markdown-like formatting
            if (typeof marked !== 'undefined') {
                return marked.parse(text);
            }
            
            // Fallback simple formatting
            return text
                .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\*(.+?)\\*/g, '<em>$1</em>')
                .replace(/`(.+?)`/g, '<code>$1</code>')
                .replace(/\\n/g, '<br>');
        }

        function addMessage(content, isUser = false, animate = true) {
            const messagesContainer = document.getElementById('chat-messages');
            const welcomeScreen = document.getElementById('welcome-screen');
            
            if (welcomeScreen) {
                welcomeScreen.style.display = 'none';
            }

            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${animate ? 'animate' : ''}`;
            
            const currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            messageDiv.innerHTML = `
                <div class="message-header">
                    <div class="avatar ${isUser ? 'user-avatar' : 'bot-avatar'}">
                        ${isUser ? '👤' : '🤖'}
                    </div>
                    <div class="message-sender">${isUser ? 'You' : 'EduBot'}</div>
                    <div class="message-time">${currentTime}</div>
                </div>
                <div class="message-content">
                    ${isUser ? content : formatMessage(content)}
                </div>
            `;
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function showTypingIndicator() {
            const messagesContainer = document.getElementById('chat-messages');
            const typingDiv = document.createElement('div');
            typingDiv.id = 'typing-indicator';
            typingDiv.className = 'message';
            typingDiv.innerHTML = `
                <div class="message-header">
                    <div class="avatar bot-avatar">🤖</div>
                    <div class="message-sender">EduBot</div>
                </div>
                <div class="typing-indicator">
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                    <span style="color: var(--text-secondary); margin-left: 8px;">thinking...</span>
                </div>
            `;
            messagesContainer.appendChild(typingDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function hideTypingIndicator() {
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }

        async function sendMessage(predefinedMessage = null) {
            const input = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const message = predefinedMessage || input.value.trim();
            
            if (!message || isTyping) return;

            if (!predefinedMessage) {
                input.value = '';
                input.style.height = 'auto';
            }
            
            addMessage(message, true);
            
            isTyping = true;
            sendButton.disabled = true;
            showTypingIndicator();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                hideTypingIndicator();
                
                if (data.error) {
                    addMessage(`❌ Error: ${data.error}`, false);
                } else {
                    addMessage(data.reply, false);
                }
            } catch (error) {
                hideTypingIndicator();
                addMessage('❌ Sorry, there was an error connecting to the server. Please try again.', false);
            } finally {
                isTyping = false;
                sendButton.disabled = false;
                input.focus();
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }

        function suggestTopic(topic) {
            const suggestions = {
                'mathematics': 'Explain calculus concepts and help me solve integration problems',
                'science': 'Teach me about photosynthesis and cellular respiration',
                'programming': 'Explain object-oriented programming principles',
                'history': 'Tell me about the Renaissance period and its impact',
                'literature': 'Analyze the themes in Shakespeare\\'s Hamlet',
                'physics': 'Explain Einstein\\'s theory of relativity'
            };
            
            sendMessage(suggestions[topic] || `Tell me about ${topic}`);
        }

        function clearChat() {
            const messagesContainer = document.getElementById('chat-messages');
            const welcomeScreen = document.getElementById('welcome-screen');
            
            messagesContainer.innerHTML = '';
            messagesContainer.appendChild(welcomeScreen);
            welcomeScreen.style.display = 'flex';
            
            fetch('/clear_history', { method: 'POST' });
        }

        // Auto-resize textarea
        document.getElementById('message-input').addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // Focus input on load
        window.addEventListener('load', () => {
            document.getElementById('message-input').focus();
        });
    </script>
</body>
</html>
    '''
    
    return html_content

def is_educational_query(query):
    """Check if the query is related to education or chat functionality."""
    query_lower = query.lower()
    
    # Accept chat history and self-reference queries
    chat_patterns = [
        r"(previous|last|earlier) (message|prompt|question)",
        r"what (did|was) (i|you) (say|ask|told|tell)",
        r"(show|display|get|fetch) (my|the) (history|conversation)",
        r"what (is|was) my",
        r"can you (remember|recall)",
        r"who (am i|are you)"
    ]
    
    for pattern in chat_patterns:
        if re.search(pattern, query_lower):
            return True
    
    # Check for educational keywords
    for domain in EDUCATIONAL_DOMAINS:
        if domain in query_lower:
            return True
            
    # Check for educational question patterns
    educational_patterns = [
        r"what (is|are|was|were) .+\?",
        r"how (do|does|can|could) .+\?",
        r"why (is|are|does|do) .+\?",
        r"explain .+",
        r"define .+",
        r"describe .+",
        r"teach me .+",
        r"learn about .+",
        r"understand .+",
        r"(help|assist) .+ (with|in) .+"
    ]
    
    for pattern in educational_patterns:
        if re.search(pattern, query_lower):
            return True
            
    return False

@app.route('/chat', methods=['POST'])
def chat():
    if not GEMINI_API_KEY or not client:
        logger.error("Google Gemini API key is missing or client initialization failed")
        return jsonify({"error": "Google Gemini API key not set. Please check your .env file."}), 500

    try:
        # Get user input from the request
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400

        user_input = data.get('message')
        logger.debug(f"Received user input: {user_input}")
        
        if not user_input:
            logger.error("No message provided in request")
            return jsonify({"error": "No message provided"}), 400
            
        # Get or create session ID
        session_id = session.get('session_id')
        if not session_id or session_id not in conversation_history:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            conversation_history[session_id] = []
        
        # Add user message to history
        conversation_history[session_id].append({
            "role": "user",
            "content": user_input
        })

        # Analyze user input with NLTK
        input_analysis = analyze_user_input(user_input)
        logger.debug(f"NLTK Analysis: {input_analysis}")

        # Check if the query is educational
        if not is_educational_query(user_input):
            bot_response = "I'm an educational assistant and can help you with academic topics like math, science, history, and literature. Could you please ask me something related to education or learning?"
            
            # Add bot response to history
            conversation_history[session_id].append({
                "role": "assistant",
                "content": bot_response
            })
            
            # Limit history size (keep last 20 messages)
            if len(conversation_history[session_id]) > 20:
                conversation_history[session_id] = conversation_history[session_id][-20:]
                
            return jsonify({
                "reply": bot_response,
                "history": conversation_history[session_id],
                "analysis": input_analysis
            })
        
        # Craft an enhanced system prompt using NLTK analysis
        enhanced_prompt = enhance_educational_prompt(user_input, input_analysis)
        
        system_prompt = f"""You are EduBot, an educational assistant focused on helping students learn while also being able to engage in natural conversation.

{enhanced_prompt}

Your primary focus is educational content, but you should also:
1. Be able to respond to questions about the conversation history
2. Answer when users ask about their previous messages or prompts
3. Remember and reference previous questions and answers when relevant

When explaining educational concepts:
- Break down complex ideas into simpler parts
- Use analogies when helpful
- Include examples to illustrate points
- Highlight key concepts or vocabulary
- Mention real-world applications when relevant
- Adjust your explanation level based on the question complexity

If someone asks to see their previous message or what they asked before, show them their previous prompt.
Maintain a conversational, friendly tone while being informative and helpful.

If you're not sure about a fact, acknowledge the uncertainty rather than providing potentially incorrect information."""

        # Prepare the content structure with conversation history
        contents = []
        
        # Add system prompt as the first message
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=system_prompt)]
            )
        )
        
        # Add previous conversation history (limited to last few exchanges for context)
        history_to_include = conversation_history[session_id][-10:] if len(conversation_history[session_id]) > 5 else conversation_history[session_id]
        
        for message in history_to_include:
            role = "user" if message["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=message["content"])]
                )
            )
            
        # Configure the content generation
        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=1024,
            response_mime_type="text/plain",
        )

        # Make the API call
        logger.debug("Sending request to Gemini 2.0 Flash")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=generate_content_config,
        )
        
        # Extract the bot's reply
        bot_reply = response.text
        
        # Add bot response to history
        conversation_history[session_id].append({
            "role": "assistant",
            "content": bot_reply
        })
        
        # Limit history size (keep last 20 messages)
        if len(conversation_history[session_id]) > 20:
            conversation_history[session_id] = conversation_history[session_id][-20:]
            
        logger.debug(f"Received response from Google Gemini: {bot_reply[:100]}...")
        return jsonify({
            "reply": bot_reply, 
            "history": conversation_history[session_id],
            "analysis": input_analysis
        })

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to fetch conversation history
@app.route('/history', methods=['GET'])
def get_history():
    session_id = session.get('session_id')
    if not session_id or session_id not in conversation_history:
        return jsonify({"history": []})
    
    return jsonify({"history": conversation_history[session_id]})

# Route to clear conversation history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    session_id = session.get('session_id')
    if session_id and session_id in conversation_history:
        conversation_history[session_id] = []
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)