import os
import json
import openai

class LegalAnalyzer:
    def __init__(self, api_key=None, provider="openrouter", model="openai/gpt-4-turbo"):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        
        if self.provider == "openrouter" and self.api_key:
            # OpenRouter uses OpenAI-compatible API
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        elif self.provider == "openai" and self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def analyze_contract(self, text, contract_type="General", nlp_data=None):
        if not self.client:
            return self._mock_analysis(text, contract_type, nlp_data)
        
        # Build enhanced context from NLP data
        context = ""
        if nlp_data:
            context = f"""
            
            Pre-extracted Information:
            - Contract Type: {nlp_data.get('contract_type', 'Unknown')}
            - Parties: {', '.join(nlp_data.get('entities', {}).get('parties', []))}
            - Detected Risk Indicators: {', '.join(nlp_data.get('risk_indicators', {}).keys())}
            - Ambiguous Terms Found: {len(nlp_data.get('ambiguities', []))}
            """
        
        prompt = f"""
        You are an expert legal advisor specializing in Indian contract law for Small and Medium Enterprises (SMEs).
        
        Analyze the following contract text thoroughly. The text may be in English, Hindi, or mixed.
        If Hindi text is present, translate key terms to English for analysis.
        {context}
        
        Contract Text (first 6000 characters):
        {text[:6000]}
        
        Provide a comprehensive legal analysis in JSON format with the following structure:
        
        {{
            "language_detected": "English/Hindi/Mixed",
            "contract_info": {{
                "type": "Employment/Vendor/Service/Lease/Partnership/NDA/Other",
                "parties": ["Party 1 name", "Party 2 name"],
                "effective_date": "extracted date or null",
                "duration": "contract duration or null",
                "jurisdiction": "city/state",
                "governing_law": "specific Indian laws mentioned",
                "key_amounts": ["financial figures mentioned"]
            }},
            "risk_assessment": {{
                "composite_score": 0-100,
                "risk_level": "Low/Medium/High",
                "summary": "2-3 sentence overview of main concerns",
                "key_risks": [
                    {{
                        "clause": "clause name/number",
                        "risk_level": "Low/Medium/High",
                        "category": "Indemnity/Termination/Non-compete/IP/Penalty/Jurisdiction/Other",
                        "explanation": "why this is risky for SME",
                        "legal_concern": "specific Indian law concern if any",
                        "suggestion": "specific alternative language or negotiation point",
                        "priority": "Critical/High/Medium/Low"
                    }}
                ]
            }},
            "clause_breakdown": [
                {{
                    "clause_number": "1.1",
                    "clause_name": "Payment Terms",
                    "original_text": "brief excerpt",
                    "simplified_explanation": "plain English explanation",
                    "obligations": ["what party must do"],
                    "rights": ["what party can do"],
                    "red_flags": ["concerning aspects"]
                }}
            ],
            "compliance_check": [
                {{
                    "law": "Indian Contract Act 1872 / Shops and Establishments Act / Payment of Wages Act / etc",
                    "section": "specific section if applicable",
                    "status": "Compliant/Warning/Non-Compliant/Unclear",
                    "notes": "specific compliance concern or confirmation",
                    "recommendation": "action needed if non-compliant"
                }}
            ],
            "unfavorable_terms": [
                {{
                    "term": "specific unfavorable term",
                    "impact": "business impact on SME",
                    "negotiation_strategy": "how to negotiate this"
                }}
            ],
            "missing_protections": [
                "important clauses that should be added"
            ],
            "overall_recommendation": {{
                "verdict": "Sign As-Is/Negotiate/Reject/Seek Legal Counsel",
                "reasoning": "why this recommendation",
                "priority_negotiations": ["top 3 items to negotiate"]
            }}
        }}
        
        Focus on:
        1. Unfair termination clauses
        2. Overly broad indemnity
        3. Unreasonable non-compete restrictions
        4. One-sided IP transfer
        5. Excessive penalties
        6. Unfavorable jurisdiction clauses
        7. Auto-renewal traps
        8. Ambiguous language
        9. Missing standard protections
        10. Compliance with Indian labor and contract laws
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Indian Legal Advisor specializing in protecting SME interests in contract negotiations. Provide practical, actionable advice in simple business language."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3  # Lower temperature for more consistent legal analysis
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e), "mock": True, **self._mock_analysis(text, contract_type, nlp_data)}

    def _mock_analysis(self, text, contract_type, nlp_data=None):
        """Enhanced mock analysis with more realistic data"""
        
        # Try to extract some basic info from text
        parties = []
        if nlp_data and 'entities' in nlp_data:
            parties = nlp_data['entities'].get('parties', [])
        if not parties:
            parties = ["Party A", "Party B"]
        
        return {
            "language_detected": "English",
            "contract_info": {
                "type": contract_type,
                "parties": parties[:2],
                "effective_date": None,
                "duration": "Not specified",
                "jurisdiction": "India",
                "governing_law": "Indian Contract Act, 1872",
                "key_amounts": []
            },
            "risk_assessment": {
                "composite_score": 65,
                "risk_level": "Medium-High",
                "summary": "⚠️ DEMO MODE: This is a mock analysis. Please provide an API key for comprehensive legal assessment. Based on quick scan, contract contains potentially unfavorable terms.",
                "key_risks": [
                    {
                        "clause": "Indemnity Clause",
                        "risk_level": "High",
                        "category": "Indemnity",
                        "explanation": "Indemnity clause appears overly broad and may hold you liable even for the other party's negligence.",
                        "legal_concern": "May violate principles of natural justice under Indian Contract Act",
                        "suggestion": "Limit indemnity to direct losses caused by your gross negligence or willful misconduct only. Add cap on liability.",
                        "priority": "Critical"
                    },
                    {
                        "clause": "Termination Terms",
                        "risk_level": "High",
                        "category": "Termination",
                        "explanation": "Unequal termination notice periods - other party can exit quickly while you're locked in.",
                        "legal_concern": "May be considered unconscionable under Section 23 of Indian Contract Act",
                        "suggestion": "Negotiate for equal notice periods (30-60 days for both parties).",
                        "priority": "Critical"
                    },
                    {
                        "clause": "Non-Compete Restriction",
                        "risk_level": "High",
                        "category": "Non-compete",
                        "explanation": "Non-compete clause is too broad in scope and duration, restricting your business opportunities.",
                        "legal_concern": "May be unenforceable as restraint of trade under Section 27 of Indian Contract Act",
                        "suggestion": "Limit to 1 year, specific geography, and narrow business scope. Consider non-solicitation instead.",
                        "priority": "High"
                    },
                    {
                        "clause": "Payment Terms",
                        "risk_level": "Medium",
                        "category": "Other",
                        "explanation": "Payment terms heavily favor the other party with long payment cycles.",
                        "legal_concern": "None specific",
                        "suggestion": "Negotiate for milestone-based payments or shorter payment cycles (15-30 days).",
                        "priority": "Medium"
                    }
                ]
            },
            "clause_breakdown": [
                {
                    "clause_number": "1",
                    "clause_name": "Scope of Services",
                    "original_text": "Services to be provided as per agreement...",
                    "simplified_explanation": "This section defines what work you need to do. Make sure it's specific and achievable.",
                    "obligations": ["Provide defined services", "Meet quality standards"],
                    "rights": ["Receive payment upon completion"],
                    "red_flags": ["Vague scope may lead to scope creep"]
                },
                {
                    "clause_number": "2",
                    "clause_name": "Confidentiality",
                    "original_text": "Both parties shall maintain confidentiality...",
                    "simplified_explanation": "You must keep business secrets private. This is standard and reasonable.",
                    "obligations": ["Protect confidential information", "Return materials on termination"],
                    "rights": ["Receive confidential treatment of your information too"],
                    "red_flags": ["Check if duration is reasonable (2-3 years typical)"]
                }
            ],
            "compliance_check": [
                {
                    "law": "Indian Contract Act, 1872",
                    "section": "Section 27 (Restraint of Trade)",
                    "status": "Warning",
                    "notes": "Non-compete clause may be too restrictive to be enforceable",
                    "recommendation": "Narrow the scope and duration of non-compete"
                },
                {
                    "law": "Payment of Wages Act, 1936",
                    "section": "General",
                    "status": "Unclear",
                    "notes": "If this is employment contract, check wage payment timelines",
                    "recommendation": "Ensure compliance with monthly payment requirements"
                }
            ],
            "unfavorable_terms": [
                {
                    "term": "Unlimited Liability",
                    "impact": "You could be liable for unlimited damages, risking your business",
                    "negotiation_strategy": "Insist on liability cap (e.g., 2x contract value) and exclude consequential damages"
                },
                {
                    "term": "Automatic Renewal",
                    "impact": "Contract auto-renews unless you give very long notice, trapping you in unfavorable terms",
                    "negotiation_strategy": "Change to opt-in renewal or reduce notice period to 30-60 days"
                }
            ],
            "missing_protections": [
                "Force majeure clause to protect against unforeseen events",
                "Clear dispute resolution mechanism (arbitration preferred over litigation)",
                "Intellectual property ownership clarity",
                "Data protection and privacy provisions",
                "Exit strategy and transition assistance terms"
            ],
            "overall_recommendation": {
                "verdict": "Negotiate",
                "reasoning": "Contract contains several high-risk clauses that heavily favor the other party. These should be negotiated before signing. The risks are manageable with proper amendments.",
                "priority_negotiations": [
                    "Equal termination rights and notice periods",
                    "Capped and limited indemnity obligations",
                    "Reasonable non-compete scope and duration"
                ]
            }
        }
