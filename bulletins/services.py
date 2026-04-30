"""
Service pour la génération et gestion des bulletins PDF.
"""
import logging
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

logger = logging.getLogger(__name__)


class BulletinService:
    """Service pour générer des bulletins PDF"""

    @staticmethod
    def generate_bulletin_pdf(submission):
        """Génère un PDF de bulletin pour une soumission"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []

            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=1
            )

            # Titre
            story.append(Paragraph("Bulletin de Note", title_style))
            story.append(Spacer(1, 0.5 * cm))

            # Infos de base
            info_data = [
                ['Date:', datetime.now().strftime('%d/%m/%Y')],
                ['Statut:', 'Générée automatiquement'],
            ]
            info_table = Table(info_data, colWidths=[3 * cm, 12 * cm])
            info_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            story.append(info_table)

            # Construire le document
            doc.build(story)
            pdf_content = buffer.getvalue()
            buffer.close()

            return pdf_content
        except Exception as e:
            logger.error(f"Erreur génération bulletin PDF: {str(e)}")
            return b""

    @staticmethod
    def generate_bulletin_professionnel(instance):
        """Génère un bulletin professionnel avec contexte"""
        try:
            pdf_content = BulletinService.generate_bulletin_pdf(instance)
            context = {
                'generated_at': datetime.now(),
                'instance': instance,
            }
            return pdf_content, context
        except Exception as e:
            logger.error(f"Erreur génération bulletin professionnel: {str(e)}")
            return b"", {}

    @staticmethod
    def _generate_digital_signature(bulletin):
        """Génère une signature numérique pour le bulletin"""
        try:
            # Créer une signature basée sur l'ID et la date
            data = f"{bulletin.id}_{datetime.now().isoformat()}".encode()
            signature = hashlib.sha256(data).hexdigest()
            return signature
        except Exception as e:
            logger.error(f"Erreur génération signature: {str(e)}")
            return ""
