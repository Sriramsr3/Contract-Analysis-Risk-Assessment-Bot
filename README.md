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
cd "folder-name"

# Install dependencies
pip install -r requirements.txt

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



## 🎨 Features Showcase

Risk Assessment Dashboard

Clause-by-Clause Analysis

Compliance Checking

Negotiation Support


## 🔧 Supported Models (via OpenRouter)
- `openai/gpt-4o-mini` ⭐ Used
- `openai/gpt-4-turbo`
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro-1.5`
- `meta-llama/llama-3.1-70b-instruct`
- `qwen/qwen-2.5-72b-instruct`
- Any other model from [OpenRouter.ai/models](https://openrouter.ai/models)


## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **NLP**: spaCy (en_core_web_sm)
- **LLM**: OpenRouter API (GPT-4, Claude, Gemini, etc.)
- **Visualization**: Plotly
- **PDF Generation**: ReportLab
- **Data Processing**: Pandas

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

## 🙏 Credits

Built with:
- **spaCy** - NLP processing
- **OpenRouter** - Multi-model LLM access
- **Streamlit** - Web framework
- **Plotly** - Visualizations
- **ReportLab** - PDF generation

---

##  Check the live demo here 
 
`https://contract-analysis-risk-assessment-bot-1.streamlit.app/`