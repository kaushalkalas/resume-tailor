# 🎯 AI Resume Tailor

A web application that helps job seekers tailor their resumes to specific job descriptions using AI. Instead of manually rewriting your resume for every job application, this app analyzes your resume and the job description, then provides specific suggestions to improve your chances of passing ATS filters and getting noticed by recruiters.

## 🔍 Problem It Solves

| Problem | Solution |
|---------|----------|
| ❌ Sending the same resume to every job | ✅ AI analyzes both resume & job description |
| ❌ Resumes don't match job keywords | ✅ Gives specific bullet improvements |
| ❌ ATS systems reject resumes before humans see them | ✅ Shows missing ATS keywords |
| ❌ Don't know how to write strong bullets | ✅ Suggests better professional summary |
| ❌ Missing important skills for specific roles | ✅ Tells which skills to add/remove |

## 👥 Target Users

- 🎓 **Fresh Graduates** – Tailoring resume for first job
- 💼 **Job Seekers** – Applying to multiple companies
- 🔄 **Career Switchers** – Moving to different domain
- 📈 **Experienced Developers** – Targeting specific senior roles

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| AI Model | Groq API (LLaMA3) |
| PDF Parsing | pdfplumber |
| Environment | python-dotenv |
| Python Version | 3.9+ |

## 📁 Project Structure

```
resume-tailor/
├── app.py                  # Main Streamlit application
├── utils/
│   ├── __init__.py         # Package initialization
│   ├── pdf_parser.py       # Extract text from PDF
│   ├── ai_engine.py        # Groq API integration
│   └── parser.py           # Parse AI response
├── requirements.txt        # Project dependencies
├── .env                    # API keys (keep private!)
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## 🚀 Quick Start

### Step 1: Get a Free Groq API Key

1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Create an API key
4. Keep it safe - you'll need it soon!

### Step 2: Clone or Setup the Project

```bash
# Navigate to the project directory
cd resume-tailor
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Add Your API Key

Edit the `.env` file and replace `your_groq_api_key_here` with your actual Groq API key:

```
GROQ_API_KEY=your_actual_api_key_here
```

⚠️ **Important:** Never share your `.env` file or API key publicly!

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Input Your Resume
- **Option 1:** Upload a PDF file
- **Option 2:** Paste your resume text directly

### Enter Job Description
Copy and paste the job description you're applying for.

### Analyze
Click the "🚀 Analyze & Suggest" button and wait for AI analysis.

### Review Suggestions
Get personalized recommendations across 5 categories:
- 📊 **ATS Match Score** – See how much your resume matches the job (0-100%)
- 📝 **Bullet Improvements** – Better ways to phrase your accomplishments
- 🔑 **Missing Keywords** – Technical terms to add from the job description
- 💡 **Summary Suggestion** – An improved professional summary
- 🛠️ **Skills Suggestions** – Which skills to add or remove

## 🧠 How It Works Behind the Scenes

```
User Input (Resume + Job Description)
           ↓
Extract Resume Text (PDF or paste)
           ↓
Send to Groq API with Smart Prompt
           ↓
AI Analyzes & Returns Structured Suggestions
           ↓
Parse Response into Organized Sections
           ↓
Display Beautiful Interactive Results
```

## 📊 What You'll Get

### ATS Match Score
A percentage showing how well your resume matches the job description (0-100%).

### Bullet Point Improvements
For each major bullet point in your resume, you'll see:
- **Original:** Your current wording
- **Improved:** Better way to phrase it
- **Reason:** Why this is better

### Missing Keywords
Two categories:
- **Must Add:** Critical technical terms from the job description
- **Nice to Add:** Additional keywords that strengthen your profile

### Professional Summary
- **Current:** What you have in your resume
- **Suggested:** AI-written summary tailored to the job

### Skills Adjustment
- **Skills to Add:** Technical and soft skills from the job description
- **Skills to Remove:** Less relevant skills for this specific role

## ⚙️ Configuration

### Environment Variables

The `.env` file stores your API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Load it with:
```bash
python-dotenv  # Automatically loads .env on startup
```

### Model Selection

Currently using `openai/gpt-oss-20b` for:
- Fast responses (2-5 seconds)
- Accurate analysis
- Free tier availability

To change models, edit `utils/ai_engine.py` line with `model=`

## 📝 Example Output

### Input
**Resume bullet:** "Worked on machine learning models"

**Job Description mentions:** Python, ML, prediction accuracy, data science

### Output
```
Original: Worked on machine learning models

Improved: Developed ML pipelines using Python & 
          Scikit-learn, improving prediction 
          accuracy by 18%

Why: More specific, includes technical keywords,
     quantifies impact
```

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Ensure you created `.env` file in the project root
- Verify your API key is pasted correctly
- Restart the app after adding the key

### "No text extracted from PDF"
- Ensure your PDF is not image-based (scanned document)
- Try uploading a text-based PDF
- Or paste the text directly option

### Slow Response (>30 seconds)
- Check your internet connection
- Groq servers might be temporarily busy
- Try again in a few moments

### Poor Suggestions
- Provide more detail in your job description
- Ensure your resume is well-formatted
- Try with a different job description

## 📚 File Documentation

### `app.py`
The main Streamlit application that:
- Manages UI and user interactions
- Orchestrates the workflow
- Displays results in beautiful tabs

### `utils/pdf_parser.py`
Handles PDF file processing:
- Accepts uploaded PDF files
- Extracts all text content
- Cleans and returns plain text

### `utils/ai_engine.py`
Manages AI analysis:
- Connects to Groq API
- Builds optimized prompts
- Sends requests to LLaMA3 model
- Returns structured suggestions

### `utils/parser.py`
Parses AI responses:
- Takes raw AI text response
- Extracts each suggestion section
- Structures into Python dictionaries
- Returns organized results

## 💡 Tips for Better Results

1. **Detailed Resume:** More detailed resumes get better suggestions
2. **Complete JD:** Paste the full job description, not just a snippet
3. **Real Experience:** AI won't fabricate - it improves existing content
4. **Multiple Analyses:** Run it for different jobs to see pattern differences
5. **Incorporate Feedback:** Apply suggestions carefully to maintain authenticity

## 🔐 Security & Privacy

- ✅ Your resume is **never stored** on our servers
- ✅ Only sent to Groq API for analysis (they secure industry-standard)
- ✅ .env file with API key is in `.gitignore` and never shared
- ✅ No tracking or analytics
- ✅ You can run locally for complete privacy

## 🤝 Contributing

Found a bug or have an idea? Contributions welcome!

## 📄 License

This project is open source and available for personal and commercial use.

## 🎓 Learning from This Project

This project demonstrates:
- **Streamlit:** Building interactive web apps with Python
- **API Integration:** Working with Groq API
- **PDF Processing:** Managing document parsing
- **LLM Prompting:** Crafting effective AI prompts
- **State Management:** Handling app state in Streamlit
- **UI/UX:** Creating beautiful, user-friendly interfaces

## 🚀 Next Steps

1. ✅ Set up and run the app
2. ✅ Test with your own resume and a job description
3. ✅ Refine your resume based on suggestions
4. ✅ Apply to more jobs with confidence!

## 📞 Support

- **Issues:** Check the troubleshooting section above
- **Groq Docs:** https://console.groq.com/docs
- **Streamlit Docs:** https://docs.streamlit.io

## 🎉 Happy Job Hunting!

Your dream job might be just one tailored resume away. Good luck! 🚀

---

**Built with ❤️ using Streamlit, Groq, and Python**
