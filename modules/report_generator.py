from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir="logs"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_pdf(self, analysis_data, filename="contract_report.pdf"):
        """Generate comprehensive PDF report from analysis data"""
        path = os.path.join(self.output_dir, filename)
        
        try:
            doc = SimpleDocTemplate(path, pagesize=letter,
                                  topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            elements = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontSize=24,
                textColor=colors.HexColor('#1a237e'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#283593'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title
            elements.append(Paragraph("⚖️ Contract Risk Assessment Report", title_style))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                                    styles['Normal']))
            elements.append(Spacer(1, 20))
            
            # Contract Information
            elements.append(Paragraph("📋 Contract Information", heading_style))
            contract_info = analysis_data.get('contract_info', {})
            
            info_data = [
                ["Contract Type:", contract_info.get('type', 'N/A')],
                ["Parties:", ', '.join(contract_info.get('parties', ['N/A']))],
                ["Jurisdiction:", contract_info.get('jurisdiction', 'N/A')],
                ["Governing Law:", contract_info.get('governing_law', 'N/A')],
            ]
            
            if contract_info.get('effective_date'):
                info_data.append(["Effective Date:", contract_info['effective_date']])
            if contract_info.get('duration'):
                info_data.append(["Duration:", contract_info['duration']])
            
            info_table = Table(info_data, colWidths=[150, 350])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a237e')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 20))
            
            # Risk Assessment
            elements.append(Paragraph("⚠️ Risk Assessment", heading_style))
            risk_assessment = analysis_data.get('risk_assessment', {})
            score = risk_assessment.get('composite_score', 0)
            risk_level = risk_assessment.get('risk_level', 'Unknown')
            
            # Risk score with color
            score_color = colors.green if score < 30 else (colors.orange if score < 70 else colors.red)
            elements.append(Paragraph(f"<b>Composite Risk Score:</b> <font color='{score_color.hexval()}'>{score}/100</font> ({risk_level})", 
                                    styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"<b>Summary:</b> {risk_assessment.get('summary', 'N/A')}", 
                                    styles['Normal']))
            elements.append(Spacer(1, 12))
            
            # Overall Recommendation
            if 'overall_recommendation' in analysis_data:
                rec = analysis_data['overall_recommendation']
                verdict = rec.get('verdict', 'Unknown')
                verdict_color = colors.green if 'Sign' in verdict else (colors.red if 'Reject' in verdict else colors.orange)
                
                elements.append(Paragraph(f"<b>Recommendation:</b> <font color='{verdict_color.hexval()}'>{verdict}</font>", 
                                        styles['Normal']))
                elements.append(Paragraph(f"{rec.get('reasoning', '')}", styles['Normal']))
                elements.append(Spacer(1, 12))
            
            # Key Risks Table
            elements.append(Paragraph("🚨 Key Risks & Recommendations", heading_style))
            
            key_risks = risk_assessment.get('key_risks', [])
            if key_risks:
                risk_data = [["Clause", "Risk Level", "Category", "Recommendation"]]
                
                for risk in key_risks[:10]:  # Limit to top 10 for PDF
                    clause = risk.get('clause', 'N/A')
                    level = risk.get('risk_level', 'Unknown')
                    category = risk.get('category', 'Other')
                    suggestion = risk.get('suggestion', 'Consult legal advisor')
                    
                    # Truncate long text
                    if len(suggestion) > 100:
                        suggestion = suggestion[:97] + "..."
                    
                    risk_data.append([clause, level, category, suggestion])
                
                risk_table = Table(risk_data, colWidths=[100, 70, 80, 250])
                risk_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('PADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(risk_table)
            else:
                elements.append(Paragraph("No specific risks identified.", styles['Normal']))
            
            elements.append(Spacer(1, 20))
            
            # Clause Breakdown
            elements.append(Paragraph("📑 Clause Analysis", heading_style))
            
            # Handle both old and new formats
            clauses = analysis_data.get('clause_breakdown', analysis_data.get('clause_explanation', []))
            
            if clauses:
                for idx, clause in enumerate(clauses[:8], 1):  # Limit to 8 clauses
                    # Handle new format (clause_breakdown)
                    if 'clause_number' in clause:
                        clause_title = f"{clause.get('clause_number', idx)}. {clause.get('clause_name', 'Unnamed Clause')}"
                        explanation = clause.get('simplified_explanation', 'N/A')
                    # Handle old format (clause_explanation)
                    else:
                        clause_title = clause.get('clause_name', f'Clause {idx}')
                        explanation = clause.get('simplified_text', 'N/A')
                    
                    elements.append(Paragraph(f"<b>{clause_title}</b>", styles['Heading3']))
                    elements.append(Paragraph(explanation, styles['Normal']))
                    
                    # Add obligations and rights if available (new format)
                    if 'obligations' in clause and clause['obligations']:
                        elements.append(Paragraph("<b>Your Obligations:</b>", styles['Normal']))
                        for ob in clause['obligations'][:3]:
                            elements.append(Paragraph(f"• {ob}", styles['Normal']))
                    
                    if 'red_flags' in clause and clause['red_flags']:
                        elements.append(Paragraph(f"<font color='red'><b>⚠️ Red Flags:</b> {', '.join(clause['red_flags'])}</font>", 
                                                styles['Normal']))
                    
                    elements.append(Spacer(1, 10))
            else:
                elements.append(Paragraph("No clause breakdown available.", styles['Normal']))
            
            elements.append(PageBreak())
            
            # Compliance Check
            elements.append(Paragraph("🇮🇳 Indian Law Compliance", heading_style))
            
            compliance = analysis_data.get('compliance_check', [])
            if compliance:
                comp_data = [["Law/Act", "Status", "Notes"]]
                
                for comp in compliance:
                    law = comp.get('law', 'N/A')
                    status = comp.get('status', 'Unknown')
                    notes = comp.get('notes', 'N/A')
                    
                    if len(notes) > 150:
                        notes = notes[:147] + "..."
                    
                    comp_data.append([law, status, notes])
                
                comp_table = Table(comp_data, colWidths=[150, 80, 270])
                comp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('PADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(comp_table)
            else:
                elements.append(Paragraph("No specific compliance issues identified.", styles['Normal']))
            
            elements.append(Spacer(1, 20))
            
            # Unfavorable Terms
            if 'unfavorable_terms' in analysis_data and analysis_data['unfavorable_terms']:
                elements.append(Paragraph("❌ Unfavorable Terms to Negotiate", heading_style))
                
                for term in analysis_data['unfavorable_terms'][:5]:
                    elements.append(Paragraph(f"<b>{term.get('term', 'N/A')}</b>", styles['Heading4']))
                    elements.append(Paragraph(f"<b>Impact:</b> {term.get('impact', 'N/A')}", styles['Normal']))
                    elements.append(Paragraph(f"<b>Strategy:</b> {term.get('negotiation_strategy', 'N/A')}", 
                                            styles['Normal']))
                    elements.append(Spacer(1, 8))
            
            # Priority Negotiations
            if 'overall_recommendation' in analysis_data and 'priority_negotiations' in analysis_data['overall_recommendation']:
                elements.append(Paragraph("🎯 Top Priority Negotiations", heading_style))
                for idx, item in enumerate(analysis_data['overall_recommendation']['priority_negotiations'], 1):
                    elements.append(Paragraph(f"{idx}. {item}", styles['Normal']))
                elements.append(Spacer(1, 12))
            
            # Footer/Disclaimer
            elements.append(Spacer(1, 20))
            disclaimer_style = ParagraphStyle(
                'Disclaimer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            elements.append(Paragraph(
                "⚠️ <b>LEGAL DISCLAIMER:</b> This report provides preliminary analysis only and is NOT legal advice. "
                "Always consult a qualified legal professional before making decisions based on this analysis.",
                disclaimer_style
            ))
            
            # Build PDF
            doc.build(elements)
            return path
            
        except Exception as e:
            # If PDF generation fails, create a simple text-based PDF
            print(f"Error generating detailed PDF: {str(e)}")
            return self._generate_simple_pdf(analysis_data, path)
    
    def _generate_simple_pdf(self, analysis_data, path):
        """Fallback simple PDF generation"""
        try:
            c = canvas.Canvas(path, pagesize=letter)
            width, height = letter
            
            y = height - 50
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, y, "Contract Risk Assessment Report")
            
            y -= 40
            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"Risk Score: {analysis_data.get('risk_assessment', {}).get('composite_score', 'N/A')}/100")
            
            y -= 30
            c.drawString(50, y, "Please see the JSON export for full details.")
            
            c.save()
            return path
        except Exception as e:
            print(f"Error in fallback PDF: {str(e)}")
            raise
