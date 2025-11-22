# � EduBot Pro - AI Educational Assistant

**Your intelligent educational companion powered by Google Gemini AI with stunning dark theme and advanced NLTK text processing!**

![EduBot Pro](https://img.shields.io/badge/EduBot-Pro-blue?style=for-the-badge&logo=graduation-cap)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-red?style=for-the-badge&logo=flask)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-yellow?style=for-the-badge&logo=google)

## 🚀 Quick Start (3 Simple Steps)

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Set Up API Key**
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a free API key
- Create a `.env` file in the project directory:
```env
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. **Run the Application**
```bash
python app.py
```
Open your browser and go to: **http://localhost:5000**

## ✨ Features

### 🎨 **Modern Dark Theme Interface**
- **Sleek Black Design** with glowing blue, purple, and gold accents
- **Smooth Animations** and transitions on all elements
- **ChatGPT-like Interface** with modern conversation layout
- **Responsive Design** that works perfectly on all devices
- **Glassmorphism Effects** with backdrop blur and transparency

### 🧠 **Advanced AI Capabilities**
- **Google Gemini 2.0 Flash** - Latest AI model for education
- **NLTK Text Processing** - Enhanced understanding of user queries
- **Smart Question Analysis** - Automatically detects question types
- **Complexity Assessment** - Adjusts responses based on question difficulty
- **Conversation Memory** - Remembers context throughout the session

### 📚 **Comprehensive Subject Coverage**
- 🧮 **Mathematics:** Algebra, Calculus, Geometry, Statistics, Probability
- 🔬 **Sciences:** Physics, Chemistry, Biology, Earth Science, Astronomy
- 💻 **Programming:** Python, JavaScript, Java, C++, Data Science, AI
- 📖 **Literature:** Analysis, Writing, Grammar, Poetry, Creative Writing
- 🏛️ **History:** World History, Historical Events, Civilizations
- 🌍 **Geography:** Physical Geography, Human Geography, Climate
- 🎨 **Arts:** Art History, Music Theory, Visual Arts
- 📊 **Social Studies:** Economics, Political Science, Psychology, Sociology

### 🔍 **NLTK-Powered Features**
- **Intelligent Tokenization** - Breaks down questions into meaningful parts
- **Key Concept Extraction** - Identifies important terms and topics
- **Question Type Detection** - Recognizes definition, procedural, conceptual questions
- **Complexity Analysis** - Estimates question difficulty for appropriate responses
- **Enhanced Prompting** - Creates optimized prompts for better AI responses

## 🎯 How to Use

1. **Start the app:** `python app.py`
2. **Open browser:** Navigate to `http://localhost:5000`
3. **Start learning:** Ask any educational question!

### � Example Questions:

#### Mathematics
```
"Explain derivatives in calculus with examples"
"How do I solve quadratic equations?"
"What's the difference between mean and median?"
```

#### Science
```
"Explain photosynthesis step by step"
"What are Newton's laws of motion?"
"How does DNA replication work?"
```

#### Programming
```
"Teach me object-oriented programming"
"How do I debug Python code effectively?"
"Explain machine learning algorithms"
```

#### Literature
```
"Analyze the themes in Romeo and Juliet"
"Help me improve my essay writing"
"What are different types of poetry?"
```

## 🔧 Technical Architecture

### **Backend**
- **Framework:** Flask 3.0 (Python web framework)
- **AI Engine:** Google Gemini 2.0 Flash
- **Text Processing:** NLTK 3.8+ for advanced language analysis
- **Session Management:** Flask sessions with secure secret keys

### **Frontend**
- **Languages:** Modern HTML5, CSS3, JavaScript
- **Styling:** Custom dark theme with CSS custom properties
- **Effects:** Smooth animations, glowing elements, glassmorphism
- **Responsive:** Mobile-first design with CSS Grid and Flexbox

### **AI Features**
- **Natural Language Understanding** via NLTK
- **Educational Content Filtering** 
- **Conversation History Management**
- **Smart Response Generation**

## 📁 Project Structure

```
EduBot-Pro/
├── 🚀 app.py              # Main Flask application (RUN THIS!)
├── � index.html          # Alternative static HTML version
├── 🎨 styles.css          # CSS styling for static version
├── ⚡ script.js           # JavaScript for static version
├── 📦 requirements.txt    # Python dependencies
├── 🔑 .env               # API keys (create this file)
├── 🚫 .gitignore         # Git ignore rules
├── 📖 README.md          # This documentation
└── 🗂️ templates/         # Flask templates (if needed)
```

## 🛠️ Dependencies

```python
flask==3.0.0              # Web framework
werkzeug==3.0.1           # WSGI utilities
google-generativeai>=0.4.0 # Google Gemini AI
python-dotenv==0.19.0     # Environment variables
markdown==3.5.1           # Markdown processing
markupsafe==2.1.3         # Safe string handling
nltk>=3.8.1               # Natural language processing
```

## 🌌 Dark Theme Showcase

### **Color Palette**
- **Primary:** Deep Black (`#0a0a0a`) - Main background
- **Secondary:** Charcoal (`#1a1a1a`, `#2a2a2a`) - Secondary surfaces
- **Accent Blue:** Electric Blue (`#03a9f4`) - User elements
- **Accent Purple:** Royal Purple (`#9c27b0`) - Bot elements  
- **Accent Gold:** Bright Gold (`#ffc107`) - Highlights and borders
- **Text:** Pure White (`#ffffff`) with secondary gray (`#b4b4b4`)

### **Visual Effects**
- ✨ **Glowing Borders** - Blue glow on focused inputs
- 🌟 **Animated Gradients** - Shifting colors on buttons
- 💫 **Smooth Transitions** - 0.3s ease-in-out on all elements
- � **Glassmorphism** - Backdrop blur effects
- 📱 **Responsive Animations** - Scale and translate effects

## 🔒 Security & Privacy

- ✅ **API Key Protection** - Stored in `.env` file, excluded from Git
- ✅ **Session Security** - Secure secret keys for session management
- ✅ **Input Validation** - NLTK-powered content filtering
- ✅ **Error Handling** - Graceful error handling for all components
- ✅ **No Data Storage** - Conversations are session-only

## 🚀 Deployment Options

### **Local Development**
```bash
python app.py
# Access at http://localhost:5000
```

### **Production Deployment**

#### **Heroku**
```bash
# Install Heroku CLI
heroku create your-edubot-app
heroku config:set GEMINI_API_KEY=your_key
heroku config:set SECRET_KEY=your_secret
git push heroku main
```

#### **Vercel**
```bash
# Install Vercel CLI
vercel
# Configure environment variables in Vercel dashboard
```

#### **Railway**
```bash
# Connect GitHub repo to Railway
# Set environment variables in Railway dashboard
```

## 📊 NLTK Analysis Features

### **Question Type Detection**
- **Definition Questions:** "What is...", "Define...", "Explain..."
- **Procedural Questions:** "How to...", "Solve...", "Calculate..."
- **Conceptual Questions:** "Why...", "Because...", "Reason..."
- **Comparison Questions:** "Compare...", "Difference...", "Similar..."

### **Complexity Assessment**
- **Low Complexity:** Simple questions, short sentences
- **Medium Complexity:** Standard educational questions
- **High Complexity:** Advanced topics, long explanations needed

### **Key Concept Extraction**
- Identifies important nouns and adjectives
- Highlights educational terms and topics
- Enhances AI prompts with relevant context

## 🎓 Educational Focus

### **Learning Objectives**
- ✅ **Explain Complex Concepts** in simple terms
- ✅ **Provide Step-by-Step Solutions** for problems
- ✅ **Give Real-World Examples** and applications
- ✅ **Encourage Critical Thinking** with follow-up questions
- ✅ **Support Multiple Learning Styles** with varied explanations

### **Subject Expertise**
- 📐 **STEM Fields** - Mathematics, Science, Technology, Engineering
- 📚 **Humanities** - Literature, History, Philosophy, Arts
- 💼 **Social Sciences** - Psychology, Sociology, Economics
- 🌍 **Languages** - Grammar, Vocabulary, Writing Skills

## 🔧 Troubleshooting

### **Common Issues**

#### **API Key Error**
```
Error: Google Gemini API key not set
Solution: Create .env file with GEMINI_API_KEY=your_key
```

#### **NLTK Download Error**
```
Error: NLTK data not found
Solution: App will auto-download, or run:
python -c "import nltk; nltk.download('all')"
```

#### **Import Error**
```
Error: No module named 'flask'
Solution: pip install -r requirements.txt
```

#### **Port Already in Use**
```
Error: Address already in use
Solution: Change port in app.py or kill existing process
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Create** a Pull Request

### **Areas for Contribution**
- 🎨 UI/UX improvements
- 🧠 Additional AI features
- 📚 More educational subjects
- 🔧 Performance optimizations
- 📖 Documentation enhancements

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - For powerful educational AI capabilities
- **NLTK Team** - For natural language processing tools
- **Flask Community** - For the excellent web framework
- **Open Source Contributors** - For inspiration and tools

## 📞 Support

Need help? Here are your options:

1. **Check the logs** - Look for error messages in the terminal
2. **Verify setup** - Ensure `.env` file has correct API key
3. **Update dependencies** - Run `pip install -r requirements.txt --upgrade`
4. **Check internet** - Ensure stable connection for AI API calls

---

## 🎯 Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Run with debug mode
export FLASK_DEBUG=1 && python app.py

# Install NLTK data manually
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Check if everything is working
curl http://localhost:5000
```

---

**🌟 Ready to revolutionize your learning experience? Start EduBot Pro now and discover the future of AI-powered education! 🚀**

*Made with ❤️ for learners everywhere*
