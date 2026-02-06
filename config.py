# Configuration file for Contract Analysis Bot

# API Configuration
API_PROVIDER = "openrouter"  # Options: "openrouter" or "openai"
API_MODEL = "openai/gpt-4o-mini"  # Model to use for analysis
API_KEY = "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"  # Add your API key here (or use environment variable)

# Alternative: Use environment variable (recommended for production)
# Set environment variable: OPENROUTER_API_KEY or OPENAI_API_KEY
# The app will automatically use it if API_KEY is empty

# Model Options (for reference)
POPULAR_MODELS = {
    "openrouter": [
        "openai/gpt-4-turbo",
        "openai/gpt-4o-mini",
        "anthropic/claude-3.5-sonnet",
        "google/gemini-pro-1.5",
        "meta-llama/llama-3.1-70b-instruct",
        "qwen/qwen-2.5-72b-instruct",
    ],
    "openai": [
        "gpt-4-turbo-preview",
        "gpt-4",
        "gpt-3.5-turbo",
    ]
}

# Application Settings
SHOW_NLP_DETAILS_DEFAULT = False
SHOW_RAW_JSON_DEFAULT = False
MAX_FILE_SIZE_MB = 10
DEFAULT_CONTRACT_TYPE = "Auto-Detect"

# NLP Settings
SPACY_MODEL = "en_core_web_sm"

# Output Settings
OUTPUT_DIR = "logs"
REPORT_FILENAME_PREFIX = "contract_report"
AUDIT_LOG_FILE = "audit_trail.json"

# UI Settings
PAGE_TITLE = "FinHealth Legal AI"
PAGE_ICON = "⚖️"
LAYOUT = "wide"
