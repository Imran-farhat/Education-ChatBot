// Educational topics and sample questions for quick suggestions
const educationalTopics = {
    'mathematics': ['Can you explain quadratic equations?', 'What is calculus used for?', 'How do I solve systems of linear equations?'],
    'science': ['Can you explain photosynthesis?', 'How does gravity work?', 'What is the periodic table?'],
    'history': ['What caused World War II?', 'Who was Mahatma Gandhi?', 'Explain the Industrial Revolution'],
    'literature': ['Can you analyze Shakespeare\'s Hamlet?', 'What are the themes in To Kill a Mockingbird?', 'Explain the significance of George Orwell\'s 1984'],
    'programming': ['How do I learn Python?', 'Explain object-oriented programming', 'What is the difference between Java and JavaScript?']
};

// Store conversation history
let chatHistory = [];
let isTyping = false;

// Configure marked options for safer rendering
marked.setOptions({
    breaks: true,
    gfm: true,
    sanitize: false,
    headerIds: false,
    mangle: false
});

// DOM elements
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const welcomeScreen = document.getElementById('welcome-screen');
const quickActions = document.getElementById('quick-actions');

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    autoResizeTextarea();
});

function setupEventListeners() {
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter (but allow Shift+Enter for new lines)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    messageInput.addEventListener('input', autoResizeTextarea);
    
    // Show quick actions when user starts typing
    messageInput.addEventListener('focus', () => {
        if (chatHistory.length === 0) {
            quickActions.style.display = 'flex';
        }
    });
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 200) + 'px';
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isTyping) return;
    
    // Hide welcome screen if it's the first message
    if (welcomeScreen) {
        welcomeScreen.style.display = 'none';
    }
    
    // Hide quick actions
    quickActions.style.display = 'none';
    
    // Add user message
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    autoResizeTextarea();
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator();
        if (data.response) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    })
    .catch(error => {
        hideTypingIndicator();
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error connecting to the server. Please try again.', 'bot');
    });
}

function addMessage(content, sender) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container';
    
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';
    
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${sender}-avatar`;
    avatar.innerHTML = sender === 'user' ? 'U' : '<i class="fas fa-graduation-cap"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'bot') {
        // Parse markdown for bot messages
        messageContent.innerHTML = marked.parse(content);
    } else {
        // Plain text for user messages
        messageContent.textContent = content;
    }
    
    messageWrapper.appendChild(avatar);
    messageWrapper.appendChild(messageContent);
    messageContainer.appendChild(messageWrapper);
    
    chatMessages.appendChild(messageContainer);
    
    // Store in history
    chatHistory.push({ sender, content, timestamp: new Date() });
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add animation
    messageContainer.style.opacity = '0';
    messageContainer.style.transform = 'translateY(20px)';
    setTimeout(() => {
        messageContainer.style.transition = 'all 0.3s ease';
        messageContainer.style.opacity = '1';
        messageContainer.style.transform = 'translateY(0)';
    }, 10);
}

function showTypingIndicator() {
    if (isTyping) return;
    isTyping = true;
    
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container typing-container';
    messageContainer.id = 'typing-indicator';
    
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar bot-avatar';
    avatar.innerHTML = '<i class="fas fa-graduation-cap"></i>';
    
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerHTML = `
        <span>EduBot is thinking</span>
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    messageWrapper.appendChild(avatar);
    messageWrapper.appendChild(typingIndicator);
    messageContainer.appendChild(messageWrapper);
    
    chatMessages.appendChild(messageContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Disable send button
    sendButton.disabled = true;
}

function hideTypingIndicator() {
    isTyping = false;
    const typingElement = document.getElementById('typing-indicator');
    if (typingElement) {
        typingElement.remove();
    }
    
    // Enable send button
    sendButton.disabled = false;
}

function useExample(exampleText) {
    messageInput.value = exampleText;
    messageInput.focus();
    autoResizeTextarea();
}

function insertText(text) {
    const currentValue = messageInput.value;
    messageInput.value = currentValue + (currentValue ? ' ' : '') + text + ' ';
    messageInput.focus();
    autoResizeTextarea();
}

function startNewChat() {
    // Clear chat history
    chatHistory = [];
    
    // Clear messages
    chatMessages.innerHTML = '';
    
    // Show welcome screen
    const welcomeHTML = `
        <div class="welcome-screen" id="welcome-screen">
            <h1 class="welcome-title">Welcome to EduBot AI</h1>
            <p class="welcome-subtitle">Your intelligent educational assistant powered by advanced AI. Ask questions, get explanations, solve problems, and learn anything!</p>
            
            <div class="example-prompts">
                <div class="example-prompt" onclick="useExample('Explain quantum physics in simple terms')">
                    <div class="example-prompt-title">
                        <i class="fas fa-atom"></i>
                        Science & Physics
                    </div>
                    <div class="example-prompt-desc">Explain quantum physics in simple terms</div>
                </div>
                
                <div class="example-prompt" onclick="useExample('Solve this calculus problem: ∫x²dx')">
                    <div class="example-prompt-title">
                        <i class="fas fa-calculator"></i>
                        Mathematics
                    </div>
                    <div class="example-prompt-desc">Solve this calculus problem: ∫x²dx</div>
                </div>
                
                <div class="example-prompt" onclick="useExample('What were the causes of World War I?')">
                    <div class="example-prompt-title">
                        <i class="fas fa-landmark"></i>
                        History
                    </div>
                    <div class="example-prompt-desc">What were the causes of World War I?</div>
                </div>
                
                <div class="example-prompt" onclick="useExample('Analyze the themes in Romeo and Juliet')">
                    <div class="example-prompt-title">
                        <i class="fas fa-book"></i>
                        Literature
                    </div>
                    <div class="example-prompt-desc">Analyze the themes in Romeo and Juliet</div>
                </div>
                
                <div class="example-prompt" onclick="useExample('Explain machine learning algorithms')">
                    <div class="example-prompt-title">
                        <i class="fas fa-robot"></i>
                        Computer Science
                    </div>
                    <div class="example-prompt-desc">Explain machine learning algorithms</div>
                </div>
                
                <div class="example-prompt" onclick="useExample('How does photosynthesis work?')">
                    <div class="example-prompt-title">
                        <i class="fas fa-seedling"></i>
                        Biology
                    </div>
                    <div class="example-prompt-desc">How does photosynthesis work?</div>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.innerHTML = welcomeHTML;
    
    // Show quick actions
    quickActions.style.display = 'flex';
    
    // Clear input
    messageInput.value = '';
    autoResizeTextarea();
}

// Legacy function for backward compatibility
function suggestTopic(topic) {
    const suggestions = educationalTopics[topic];
    if (suggestions && suggestions.length > 0) {
        const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
        useExample(randomSuggestion);
    }
}