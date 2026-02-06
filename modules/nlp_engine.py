import spacy
import PyPDF2
from docx import Document
import os
import re
from collections import defaultdict

class NLPEngine:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not found, try to download it
            print("Downloading spaCy model...")
            try:
                os.system("python -m spacy download en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            except Exception as e:
                print(f"Warning: Could not load spaCy model. Using basic NLP. Error: {e}")
                # Create a minimal nlp object for basic functionality
                self.nlp = None
        
        # Contract type keywords
        self.contract_keywords = {
            "Employment": ["employment", "employee", "employer", "salary", "designation", "probation", "resignation"],
            "Vendor": ["vendor", "supplier", "procurement", "delivery", "purchase order"],
            "Service": ["service agreement", "services", "service provider", "deliverables", "scope of work"],
            "Lease": ["lease", "lessor", "lessee", "rent", "premises", "tenancy"],
            "Partnership": ["partnership", "partner", "profit sharing", "capital contribution", "partnership deed"],
            "NDA": ["non-disclosure", "confidential information", "confidentiality", "proprietary"],
        }
        
        # Risk indicator keywords
        self.risk_keywords = {
            "indemnity": ["indemnify", "indemnification", "hold harmless", "defend"],
            "termination": ["terminate", "termination", "cancel", "cancellation"],
            "penalty": ["penalty", "liquidated damages", "fine", "forfeiture"],
            "non_compete": ["non-compete", "non compete", "restrictive covenant", "competition"],
            "auto_renewal": ["auto-renew", "automatic renewal", "automatically renew"],
            "jurisdiction": ["jurisdiction", "governing law", "arbitration", "dispute resolution"],
            "ip_transfer": ["intellectual property", "ip rights", "copyright", "patent", "trademark"],
        }

    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def extract_text_from_docx(self, file_path):
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    def extract_text_from_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def process_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return self.extract_text_from_docx(file_path)
        elif ext == ".txt":
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def classify_contract_type(self, text):
        """Classify contract type based on keyword matching"""
        text_lower = text.lower()
        scores = {}
        
        for contract_type, keywords in self.contract_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[contract_type] = score
        
        # Return type with highest score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return "General"

    def extract_clauses(self, text):
        """Extract numbered clauses and sub-clauses from contract"""
        clauses = []
        
        # Pattern for numbered clauses: 1., 1.1, etc.
        clause_pattern = r'(\d+\.(?:\d+\.?)*)\s+([A-Z][^\n]+(?:\n(?!\d+\.)[^\n]+)*)'
        matches = re.finditer(clause_pattern, text)
        
        for match in matches:
            clause_num = match.group(1)
            clause_text = match.group(2).strip()
            clauses.append({
                "number": clause_num,
                "text": clause_text[:500],  # Limit length
                "full_text": clause_text
            })
        
        # If no numbered clauses found, try section headers
        if not clauses:
            section_pattern = r'([A-Z][A-Z\s]+):\s*([^\n]+(?:\n(?![A-Z][A-Z\s]+:)[^\n]+)*)'
            matches = re.finditer(section_pattern, text)
            
            for idx, match in enumerate(matches, 1):
                section_name = match.group(1).strip()
                section_text = match.group(2).strip()
                clauses.append({
                    "number": str(idx),
                    "name": section_name,
                    "text": section_text[:500],
                    "full_text": section_text
                })
        
        return clauses

    def get_enhanced_entities(self, text):
        """Enhanced NER with contract-specific entities"""
        entities = {
            "parties": [],
            "persons": [],
            "organizations": [],
            "dates": [],
            "amounts": [],
            "locations": [],
            "durations": [],
        }
        
        if self.nlp is not None:
            try:
                doc = self.nlp(text[:100000])  # Limit for performance
                
                for ent in doc.ents:
                    if ent.label_ == "ORG":
                        entities["organizations"].append(ent.text)
                    elif ent.label_ == "PERSON":
                        entities["persons"].append(ent.text)
                    elif ent.label_ == "GPE":
                        entities["locations"].append(ent.text)
                    elif ent.label_ == "DATE":
                        entities["dates"].append(ent.text)
                    elif ent.label_ == "MONEY":
                        entities["amounts"].append(ent.text)
                    elif ent.label_ == "TIME":
                        entities["durations"].append(ent.text)
                
                # Extract parties (usually first 2 organizations mentioned)
                if entities["organizations"]:
                    entities["parties"] = entities["organizations"][:2]
                
                # Deduplicate
                for key in entities:
                    entities[key] = list(set(entities[key]))
            except Exception as e:
                print(f"Error in NER: {e}")
        
        # Extract CIN, GST numbers using regex (works without spaCy)
        entities["cin"] = re.findall(r'CIN:\s*([A-Z0-9]{21})', text)
        entities["gst"] = re.findall(r'GST:\s*(\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d{1}[A-Z]{1}\d{1})', text)
        
        return entities

    def identify_obligations_rights(self, text):
        """Identify obligations, rights, and prohibitions in contract"""
        obligations = []
        rights = []
        prohibitions = []
        
        # Keywords for classification
        obligation_verbs = ["shall", "must", "will", "agrees to", "undertakes to", "required to"]
        right_verbs = ["may", "entitled to", "has the right", "can", "permitted to"]
        prohibition_verbs = ["shall not", "must not", "prohibited", "forbidden", "may not"]
        
        if self.nlp is not None:
            try:
                doc = self.nlp(text[:50000])
                
                for sent in doc.sents:
                    sent_text = sent.text.lower()
                    
                    # Check for prohibitions first (more specific)
                    if any(verb in sent_text for verb in prohibition_verbs):
                        prohibitions.append(sent.text.strip())
                    # Then obligations
                    elif any(verb in sent_text for verb in obligation_verbs):
                        obligations.append(sent.text.strip())
                    # Then rights
                    elif any(verb in sent_text for verb in right_verbs):
                        rights.append(sent.text.strip())
            except Exception as e:
                print(f"Error in obligations/rights detection: {e}")
        else:
            # Fallback: simple sentence splitting
            sentences = re.split(r'[.!?]+', text[:50000])
            for sent in sentences:
                sent_text = sent.lower()
                if any(verb in sent_text for verb in prohibition_verbs):
                    prohibitions.append(sent.strip())
                elif any(verb in sent_text for verb in obligation_verbs):
                    obligations.append(sent.strip())
                elif any(verb in sent_text for verb in right_verbs):
                    rights.append(sent.strip())
        
        return {
            "obligations": obligations[:10],  # Limit to top 10
            "rights": rights[:10],
            "prohibitions": prohibitions[:10]
        }

    def detect_risk_indicators(self, text):
        """Detect presence of high-risk clause types"""
        text_lower = text.lower()
        detected_risks = {}
        
        for risk_type, keywords in self.risk_keywords.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                detected_risks[risk_type] = {
                    "present": True,
                    "keywords_found": matches
                }
        
        return detected_risks

    def detect_ambiguities(self, text):
        """Detect potentially ambiguous language"""
        ambiguous_phrases = [
            "reasonable", "best efforts", "as soon as possible", "promptly",
            "appropriate", "sufficient", "adequate", "material", "substantial"
        ]
        
        text_lower = text.lower()
        found_ambiguities = []
        
        for phrase in ambiguous_phrases:
            if phrase in text_lower:
                # Find context around the phrase
                pattern = r'.{0,50}' + re.escape(phrase) + r'.{0,50}'
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    found_ambiguities.append({
                        "phrase": phrase,
                        "context": matches[0]
                    })
        
        return found_ambiguities[:5]  # Limit to 5

    def get_basic_entities(self, text):
        """Legacy method for backward compatibility"""
        return self.get_enhanced_entities(text)
