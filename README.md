# ⚖️ Contract Analysis & Risk Assessment Bot

> **AI-Powered Legal Assistant for Indian SMEs**

A sophisticated GenAI-powered legal assistant that helps small and medium business owners understand complex contracts, identify potential legal risks, and receive actionable advice in plain language.

![Risk Assessment](https://img.shields.io/badge/Risk%20Assessment-AI%20Powered-blue)
![Indian Law](https://img.shields.io/badge/Indian%20Law-Compliant-green)
![Multilingual](https://img.shields.io/badge/Languages-English%20%7C%20Hindi-orange)

## 🎯 Key Features

### 📊 Comprehensive Analysis
- **Contract Type Classification**: Automatically identifies Employment, Vendor, Service, Lease, Partnership, NDA contracts
- **Risk Scoring**: 0-100 composite risk score with clause-level assessments
- **Plain Language Explanations**: Simplifies complex legal jargon
- **Indian Law Compliance**: Checks against Indian Contract Act, Labor Laws, GST Act

### 🔍 Advanced NLP Capabilities
- **Named Entity Recognition**: Extracts parties, dates, amounts, CIN/GST numbers
- **Clause Extraction**: Identifies and categorizes contract clauses
- **Obligation/Right/Prohibition Detection**: Classifies contractual terms
- **Ambiguity Detection**: Flags vague language like "reasonable", "best efforts"
- **Risk Indicator Detection**: Identifies penalty clauses, indemnity, non-compete, IP transfer

### 🇮🇳 Indian SME Focus
- **Multilingual Support**: English and Hindi contracts
- **Local Law Context**: Indian Contract Act 1872, Payment of Wages Act, etc.
- **SME-Friendly Templates**: Standard contracts for common scenarios
- **Negotiation Strategies**: Practical advice for unfavorable terms

### 📑 Professional Outputs
- **PDF Reports**: Downloadable assessment reports
- **Audit Trails**: JSON-based logging for compliance
- **Detailed Breakdowns**: Clause-by-clause analysis
- **Visual Dashboards**: Interactive risk gauges and charts

## 🚀 Quick Start

### Installation

```bash
# Clone or download the project
cd "Data Science"

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Get API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/) and sign up
2. Add credits to your account
3. Generate an API key

### Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Usage

1. **Configure Settings** (Sidebar):
   - Select "openrouter" as provider
   - Enter model name: `openai/gpt-4-turbo` (recommended)
   - Paste your API key

2. **Upload Contract**:
   - Supports PDF, DOCX, TXT formats
   - Max size: 10MB

3. **Review Analysis**:
   - NLP extraction happens automatically
   - Click "Analyze Contract with AI" for full assessment

4. **Explore Results**:
   - Risk score and recommendation
   - Clause breakdown
   - Compliance check
   - Unfavorable terms
   - Negotiation strategies

5. **Export**:
   - Download PDF report
   - Export JSON data
   - Log to audit trail

## 📁 Project Structure

```
Contract Analysis Bot/
├── app.py                      # Main Streamlit application
├── modules/
│   ├── nlp_engine.py          # NLP processing & entity extraction
│   ├── legal_analyzer.py      # LLM-based risk assessment
│   ├── report_generator.py    # PDF report generation
│   └── templates.py           # Standard contract templates
├── data/                      # Sample contracts & uploads
│   ├── comprehensive_vendor_contract.txt
│   ├── employment_contract_hindi.txt
│   └── sample_contract.txt
├── logs/                      # Audit trails
├── requirements.txt           # Dependencies
├── README.md                  # This file
└── DOCUMENTATION.md           # Detailed documentation
```

## 🎨 Features Showcase

### Risk Assessment Dashboard
- **Interactive Gauge**: Visual 0-100 risk score
- **Color-Coded Risks**: Critical (red), High (orange), Medium (yellow), Low (green)
- **Verdict Card**: Clear recommendation (Sign/Negotiate/Reject/Seek Counsel)

### Clause-by-Clause Analysis
- **Plain English Explanations**: Simplifies legal language
- **Obligations vs Rights**: Clear breakdown of what you must do vs what you can do
- **Red Flags**: Highlights concerning aspects

### Compliance Checking
- **Indian Contract Act 1872**: Section 23, 27 compliance
- **Labor Laws**: Payment of Wages Act, Shops & Establishments
- **Tax Laws**: GST Act compliance

### Negotiation Support
- **Unfavorable Terms**: Identifies one-sided clauses
- **Impact Analysis**: Business consequences explained
- **Negotiation Strategies**: Specific tactics for each issue
- **Priority List**: Top 3 items to negotiate

## 🔧 Supported Models (via OpenRouter)

- `openai/gpt-4-turbo` ⭐ Recommended
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro-1.5`
- `meta-llama/llama-3.1-70b-instruct`
- `qwen/qwen-2.5-72b-instruct`
- Any other model from [OpenRouter.ai/models](https://openrouter.ai/models)

## 📊 Sample Contracts

Three sample contracts are included for testing:

1. **Vendor Contract** (English) - High-risk clauses including:
   - Unequal termination rights
   - Unlimited indemnity
   - 5-year non-compete
   - Auto-renewal
   - Harsh penalties

2. **Employment Contract** (Hindi) - Unfair labor terms:
   - 60-hour work week
   - Unequal notice periods
   - 7-year non-compete
   - Minimal leave

3. **Service Agreement** (English) - Basic contract for quick testing

## ⚖️ Legal Disclaimer

**IMPORTANT**: This tool provides preliminary analysis only and is NOT a substitute for professional legal advice.

- Always consult a qualified legal professional before signing contracts
- The analysis is based on AI interpretation and may not catch all issues
- Indian law is complex and context-dependent
- Use this tool as a starting point for legal review, not as final authority

## 🔒 Privacy & Security

- **Local NLP Processing**: Entity extraction runs on your machine
- **No Data Storage**: Contracts are not permanently stored
- **Optional Audit Logs**: You control what gets logged
- **Secure API**: API keys are password-masked

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **NLP**: spaCy (en_core_web_sm)
- **LLM**: OpenRouter API (GPT-4, Claude, Gemini, etc.)
- **Visualization**: Plotly
- **PDF Generation**: ReportLab
- **Data Processing**: Pandas

## 📖 Documentation

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

Topics covered:
- Complete feature list
- Architecture details
- API integration guide
- Output structure
- Troubleshooting
- Use cases

## 🎯 Use Cases

### For Business Owners
- Review vendor agreements before signing
- Understand employment contracts
- Negotiate better terms
- Identify hidden risks

### For Legal Consultants
- Quick preliminary assessment
- Client education
- Risk identification
- Template comparison

### For Startups
- Investor agreement review
- Partnership deed analysis
- Service contract evaluation
- IP protection

## 🔄 Roadmap

- [ ] Support for more Indian languages (Tamil, Telugu, Bengali)
- [ ] Contract comparison feature
- [ ] Clause library with precedents
- [ ] Email integration
- [ ] Mobile app
- [ ] API for integration

## 🤝 Contributing

This is an educational project. Suggestions and improvements are welcome!

## 📞 Support

For issues:
1. Check [DOCUMENTATION.md](DOCUMENTATION.md)
2. Review sample contracts
3. Test with mock mode (no API key)
4. Verify dependencies

## 🙏 Credits

Built with:
- **spaCy** - NLP processing
- **OpenRouter** - Multi-model LLM access
- **Streamlit** - Web framework
- **Plotly** - Visualizations
- **ReportLab** - PDF generation

---

**Version**: 1.0  
**Focus**: Indian Contract Law for SMEs  
**License**: Educational Use  

Made with ❤️ for Indian Small & Medium Enterprises
