TEMPLATES = {
    "Employment Agreement": """
    EMPLOYMENT AGREEMENT
    
    This AGREEMENT is made on [Date] between [Company Name] and [Employee Name].
    
    1. POSITION: The Employee is hired as [Job Title].
    2. COMPENSATION: Monthly salary of INR [Amount].
    3. TERMINATION: Either party may terminate with [30] days notice.
    4. CONFIDENTIALITY: The Employee shall not disclose company secrets...
    """,
    "Non-Disclosure Agreement (NDA)": """
    NON-DISCLOSURE AGREEMENT
    
    1. PURPOSE: To share information regarding [Project Name].
    2. DEFINITION: Confidential information includes [List].
    3. DURATION: 2 years from disclosure.
    4. JURISDICTION: Courts of [City], India.
    """,
    "Service Contract": """
    SERVICE AGREEMENT
    
    1. SERVICES: [Description of services].
    2. PAYMENT: [Amount] payable upon completion.
    3. INDEMNITY: Parties agree to compensate for direct losses only.
    4. ARBITRATION: Disputes shall be settled via arbitration in [City].
    """
}

def get_template(name):
    return TEMPLATES.get(name, "Template not found.")

def list_templates():
    return list(TEMPLATES.keys())
