import streamlit as st
import os
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from modules.nlp_engine import NLPEngine
from modules.legal_analyzer import LegalAnalyzer
from modules.report_generator import ReportGenerator
from modules.templates import list_templates, get_template
import config

# Page Config
st.set_page_config(
    page_title=config.PAGE_TITLE, 
    page_icon=config.PAGE_ICON, 
    layout=config.LAYOUT
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .risk-critical { 
        color: #dc3545; 
        font-weight: bold;
        background: #ffe5e5;
        padding: 8px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .risk-high { 
        color: #fd7e14; 
        font-weight: bold;
        background: #fff3e0;
        padding: 8px;
        border-radius: 5px;
        border-left: 4px solid #fd7e14;
    }
    .risk-medium { 
        color: #ffc107; 
        font-weight: bold;
        background: #fffbea;
        padding: 8px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .risk-low { 
        color: #28a745; 
        font-weight: bold;
        background: #e8f5e9;
        padding: 8px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .card {
        padding: 25px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .metric-card {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .verdict-negotiate {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
    }
    .verdict-reject {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
    }
    .verdict-sign {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load API Configuration from config file or environment variables
api_provider = config.API_PROVIDER
selected_model = config.API_MODEL

# Try to get API key from config, then environment variables
api_key = config.API_KEY
if not api_key:
    # Try environment variables
    if api_provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY", "")
    else:
        api_key = os.getenv("OPENAI_API_KEY", "")

# Sidebar - Simplified
st.sidebar.title("🛠️ Settings")
st.sidebar.markdown("### 📊 Analysis Options")
contract_type_manual = st.sidebar.selectbox(
    "Override Contract Type", 
    [config.DEFAULT_CONTRACT_TYPE, "Employment", "Vendor", "Lease", "Partnership", "Service"]
)
show_nlp_details = st.sidebar.checkbox("Show NLP Analysis Details", value=config.SHOW_NLP_DETAILS_DEFAULT)
show_raw_json = st.sidebar.checkbox("Show Raw JSON Output", value=config.SHOW_RAW_JSON_DEFAULT)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Configuration")
st.sidebar.info(f"""
**Provider:** {api_provider}  
**Model:** {selected_model}  
**API Key:** {'✅ Configured' if api_key else '❌ Missing'}
""")

if not api_key:
    st.sidebar.warning("⚠️ No API key found. Add it to `config.py` or set environment variable.")
    st.sidebar.markdown("""
    **To configure:**
    1. Edit `config.py` and add your API key
    2. Or set environment variable:
       - `OPENROUTER_API_KEY` for OpenRouter
       - `OPENAI_API_KEY` for OpenAI
    """)

# Initialize Engines
nlp_engine = NLPEngine()
report_gen = ReportGenerator(output_dir=config.OUTPUT_DIR)
analyzer = LegalAnalyzer(api_key=api_key, provider=api_provider, model=selected_model)

# Main UI
st.title("⚖️ Contract Analysis & Risk Assessment Bot")
st.markdown("### AI-Powered Legal Assistant for Indian SMEs")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Upload Contract")
    uploaded_file = st.file_uploader("Upload PDF, DOCX or TXT file", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("🔍 Extracting and analyzing text..."):
            # Extract text
            text = nlp_engine.process_file(file_path)
            st.success(f"✅ Extracted {len(text)} characters")
            
            # Run NLP analysis
            contract_type_detected = nlp_engine.classify_contract_type(text)
            entities = nlp_engine.get_enhanced_entities(text)
            clauses = nlp_engine.extract_clauses(text)
            obligations_rights = nlp_engine.identify_obligations_rights(text)
            risk_indicators = nlp_engine.detect_risk_indicators(text)
            ambiguities = nlp_engine.detect_ambiguities(text)
            
            # Store in session
            st.session_state['contract_text'] = text
            st.session_state['nlp_data'] = {
                'contract_type': contract_type_detected,
                'entities': entities,
                'clauses': clauses,
                'obligations_rights': obligations_rights,
                'risk_indicators': risk_indicators,
                'ambiguities': ambiguities
            }
            
            st.info(f"📋 **Detected Type:** {contract_type_detected}")
            
            if st.button("🚀 Analyze Contract with AI", type="primary"):
                with st.spinner("🤖 Running comprehensive legal analysis..."):
                    final_type = contract_type_manual if contract_type_manual != "Auto-Detect" else contract_type_detected
                    results = analyzer.analyze_contract(
                        text, 
                        contract_type=final_type,
                        nlp_data=st.session_state['nlp_data']
                    )
                    st.session_state['analysis_results'] = results
                    st.success("✅ Analysis Complete!")
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NLP Details Section
    if show_nlp_details and 'nlp_data' in st.session_state:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔬 NLP Analysis Details")
        nlp_data = st.session_state['nlp_data']
        
        with st.expander("📊 Extracted Entities"):
            ent_data = nlp_data['entities']
            st.write(f"**Parties:** {', '.join(ent_data.get('parties', []))}")
            st.write(f"**Organizations:** {', '.join(ent_data.get('organizations', []))}")
            st.write(f"**Dates:** {', '.join(ent_data.get('dates', []))}")
            st.write(f"**Amounts:** {', '.join(ent_data.get('amounts', []))}")
            
        with st.expander("⚠️ Risk Indicators Detected"):
            for risk_type, data in nlp_data['risk_indicators'].items():
                st.write(f"**{risk_type.replace('_', ' ').title()}:** {', '.join(data['keywords_found'])}")
        
        with st.expander("🔍 Ambiguous Language"):
            for amb in nlp_data['ambiguities']:
                st.warning(f"**'{amb['phrase']}'** - {amb['context'][:100]}...")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Templates Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📜 Standard Templates")
    template_name = st.selectbox("Select a Template", list_templates())
    if st.button("View Template"):
        st.code(get_template(template_name), language="text")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if 'analysis_results' in st.session_state:
        results = st.session_state['analysis_results']
        
        # Risk Summary Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Risk Assessment")
        
        score = results['risk_assessment']['composite_score']
        risk_level = results['risk_assessment'].get('risk_level', 'Medium')
        
        # Risk Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            title = {'text': "Risk Score", 'font': {'size': 24}},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 30], 'color': "#d4edda"},
                    {'range': [30, 70], 'color': "#fff3cd"},
                    {'range': [70, 100], 'color': "#f8d7da"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, width="stretch")
        
        st.markdown(f"**Risk Level:** {risk_level}")
        st.write(results['risk_assessment']['summary'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Overall Recommendation
        if 'overall_recommendation' in results:
            rec = results['overall_recommendation']
            verdict = rec.get('verdict', 'Unknown')
            
            verdict_class = "verdict-sign" if "Sign" in verdict else ("verdict-reject" if "Reject" in verdict else "verdict-negotiate")
            
            st.markdown(f'<div class="{verdict_class}">', unsafe_allow_html=True)
            st.markdown(f"### 🎯 Recommendation: **{verdict}**")
            st.write(rec.get('reasoning', ''))
            st.markdown('</div>', unsafe_allow_html=True)

# Detailed Analysis Tabs
if 'analysis_results' in st.session_state:
    results = st.session_state['analysis_results']
    
    st.markdown("---")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Clause Breakdown", 
        "⚠️ Key Risks", 
        "🇮🇳 Compliance", 
        "❌ Unfavorable Terms",
        "📑 Export & Audit",
        "🔧 Raw Data"
    ])
    
    with tab1:
        st.subheader("Plain Language Clause Explanations")
        
        if 'clause_breakdown' in results:
            for clause in results['clause_breakdown']:
                with st.expander(f"📌 Clause {clause.get('clause_number', 'N/A')}: {clause.get('clause_name', 'Unnamed')}"):
                    st.markdown(f"**Original:** {clause.get('original_text', 'N/A')}")
                    st.info(f"**Plain English:** {clause.get('simplified_explanation', 'N/A')}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**Your Obligations:**")
                        for ob in clause.get('obligations', []):
                            st.write(f"- {ob}")
                    with col_b:
                        st.markdown("**Your Rights:**")
                        for right in clause.get('rights', []):
                            st.write(f"- {right}")
                    
                    if clause.get('red_flags'):
                        st.warning("🚩 **Red Flags:** " + ", ".join(clause['red_flags']))
        else:
            # Fallback to old format
            for item in results.get('clause_explanation', []):
                with st.expander(f"Clause: {item['clause_name']}"):
                    st.write(item['simplified_text'])
                    
    with tab2:
        st.subheader("High & Critical Risk Terms")
        
        risks = results['risk_assessment']['key_risks']
        
        # Group by priority
        critical_risks = [r for r in risks if r.get('priority') == 'Critical' or r.get('risk_level') == 'High']
        other_risks = [r for r in risks if r not in critical_risks]
        
        if critical_risks:
            st.error("### 🚨 Critical Risks - Immediate Attention Required")
            for risk in critical_risks:
                priority = risk.get('priority', risk.get('risk_level', 'High'))
                color_class = "risk-critical" if priority == "Critical" else "risk-high"
                
                st.markdown(f"<div class='{color_class}'>", unsafe_allow_html=True)
                st.markdown(f"**📍 {risk.get('clause', 'Unknown Clause')}** - {risk.get('category', 'General')}")
                st.markdown(f"**Risk Level:** {risk.get('risk_level', 'Unknown')}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.warning(f"**⚠️ Issue:** {risk.get('explanation', 'No explanation')}")
                if risk.get('legal_concern'):
                    st.error(f"**⚖️ Legal Concern:** {risk['legal_concern']}")
                st.success(f"**💡 Suggested Action:** {risk.get('suggestion', 'Consult legal advisor')}")
                st.markdown("---")
        
        if other_risks:
            st.warning("### ⚠️ Other Risks to Consider")
            for risk in other_risks:
                with st.expander(f"{risk.get('clause', 'Unknown')} - {risk.get('risk_level', 'Medium')}"):
                    st.write(f"**Issue:** {risk.get('explanation', '')}")
                    st.info(f"**Suggestion:** {risk.get('suggestion', '')}")
                    
    with tab3:
        st.subheader("Indian Law Compliance Check")
        
        compliance_data = results.get('compliance_check', [])
        
        # Create DataFrame for better visualization
        if compliance_data:
            df_comp = pd.DataFrame(compliance_data)
            
            # Color code by status
            def color_status(val):
                if val == "Compliant":
                    return 'background-color: #d4edda'
                elif val == "Warning":
                    return 'background-color: #fff3cd'
                elif val == "Non-Compliant":
                    return 'background-color: #f8d7da'
                return ''
            
            if 'status' in df_comp.columns:
                styled_df = df_comp.style.map(color_status, subset=['status'])
                st.dataframe(styled_df, width="stretch")
            else:
                st.dataframe(df_comp, width="stretch")
            
            # Detailed view
            for comp in compliance_data:
                if comp.get('status') in ['Warning', 'Non-Compliant']:
                    with st.expander(f"⚠️ {comp.get('law', 'Unknown Law')} - {comp.get('status')}"):
                        st.write(f"**Section:** {comp.get('section', 'N/A')}")
                        st.write(f"**Notes:** {comp.get('notes', 'N/A')}")
                        if comp.get('recommendation'):
                            st.info(f"**Recommendation:** {comp['recommendation']}")
        else:
            st.info("No specific compliance issues detected. However, consult with a legal professional for thorough compliance review.")
            
    with tab4:
        st.subheader("Unfavorable Terms & Negotiation Strategies")
        
        if 'unfavorable_terms' in results:
            for term in results['unfavorable_terms']:
                st.markdown(f"### ❌ {term.get('term', 'Unfavorable Term')}")
                st.error(f"**Impact:** {term.get('impact', 'N/A')}")
                st.success(f"**Negotiation Strategy:** {term.get('negotiation_strategy', 'N/A')}")
                st.markdown("---")
        
        if 'missing_protections' in results:
            st.subheader("🛡️ Missing Protections")
            st.info("Consider adding these clauses to protect your interests:")
            for protection in results['missing_protections']:
                st.write(f"- {protection}")
        
        if 'overall_recommendation' in results and 'priority_negotiations' in results['overall_recommendation']:
            st.subheader("🎯 Top Priority Negotiations")
            for idx, item in enumerate(results['overall_recommendation']['priority_negotiations'], 1):
                st.markdown(f"**{idx}.** {item}")
        
    with tab5:
        st.subheader("Export & Audit Trail")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            if st.button("📄 Generate PDF Report"):
                try:
                    report_path = report_gen.generate_pdf(results)
                    with open(report_path, "rb") as f:
                        st.download_button(
                            "⬇️ Download Assessment Report", 
                            f, 
                            file_name=f"Legal_Assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                    st.success("✅ Report generated successfully!")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
        
        with col_exp2:
            if st.button("💾 Log to Audit Trail"):
                audit_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "contract_type": results.get('contract_info', {}).get('type', 'Unknown'),
                    "risk_score": results['risk_assessment']['composite_score'],
                    "verdict": results.get('overall_recommendation', {}).get('verdict', 'Unknown'),
                    "file_name": uploaded_file.name if uploaded_file else "Unknown"
                }
                
                os.makedirs("logs", exist_ok=True)
                with open("logs/audit_trail.json", "a") as f:
                    f.write(json.dumps(audit_entry) + "\n")
                st.success("✅ Analysis logged successfully!")
        
        # Export JSON
        st.subheader("📤 Export Full Analysis")
        json_str = json.dumps(results, indent=2)
        st.download_button(
            "Download JSON",
            json_str,
            file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with tab6:
        if show_raw_json:
            st.subheader("🔧 Raw JSON Output")
            st.json(results)
        else:
            st.info("Enable 'Show Raw JSON Output' in the sidebar to view raw data")

else:
    st.info("👆 Upload a contract and click 'Analyze' to see comprehensive legal analysis")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>⚖️ <b>Contract Analysis & Risk Assessment Bot</b> - Empowering Indian SMEs with AI-Powered Contract Analysis</p>
        <p style='font-size: 0.9em;'>⚠️ This tool provides preliminary analysis only. Always consult a qualified legal professional before making decisions.</p>
    </div>
    """, unsafe_allow_html=True)
