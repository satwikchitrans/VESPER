import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Palette
COLOR_NAVY = colors.HexColor("#213d77")
COLOR_ORANGE = colors.HexColor("#fb792b")
COLOR_DARK = colors.HexColor("#1A202C")
COLOR_LIGHT_BG = colors.HexColor("#F7FAFC")
COLOR_BORDER = colors.HexColor("#CBD5E0")
COLOR_RED_TEXT = colors.HexColor("#C53030")

class SimpleNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header
        if self._pageNumber > 1:
            self.drawString(54, 750, "PROJECT VESPER — Simple Tech Stack & Justification Guide")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 742, 558, 742)

        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 45, 558, 45)

        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.drawString(54, 32, "VESPER | SIH 2026 | Simple Technical Overview")
        self.restoreState()


def build_simple_pdf(filename="VESPER_Tech_Stack_Simple_Guide.pdf"):
    pdf_path = os.path.join(os.getcwd(), filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=COLOR_NAVY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=COLOR_ORANGE,
        spaceAfter=12
    )

    cat_heading_style = ParagraphStyle(
        'CatHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=COLOR_NAVY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=COLOR_NAVY
    )

    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=COLOR_DARK
    )

    story = []

    # Title Banner
    story.append(Paragraph("PROJECT VESPER — Simple Tech Stack Guide", title_style))
    story.append(Paragraph("What is used, Why it is used, Where it is used & Why alternatives were rejected", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_NAVY, spaceBefore=0, spaceAfter=10))

    categories = [
        {
            "cat_title": "1. FRONTEND & MAP CONSOLE",
            "items": [
                {
                    "name": "Vanilla CSS3 (Official Government Command Theme)",
                    "what": "Plain CSS styling using official government/BEL colors (#213d77 Navy, #fb792b Saffron Accent).",
                    "why": "Loads instantly, high contrast for 24/7 control rooms, 100% compliant with government rules.",
                    "where": "Command Center control dashboard styling.",
                    "substitute": "TailwindCSS / Bootstrap.",
                    "why_not": "Heavy CSS frameworks add bloat and make dashboards look like generic commercial websites."
                },
                {
                    "name": "Vanilla JavaScript & SVG Icons",
                    "what": "Pure JavaScript with clean vector SVG icons (zero emojis/unicode characters).",
                    "why": "Zero lag during fast live updates and 100% consistent icon rendering on any police screen.",
                    "where": "Dashboard buttons, tabs, live updates, and panel docking logic.",
                    "substitute": "React.js / FontAwesome / Emojis.",
                    "why_not": "React adds rendering delay during fast map updates. Emojis show up broken on defense/police hardware."
                },
                {
                    "name": "Leaflet.js + OpenStreetMap",
                    "what": "Free open-source map engine and road vector data.",
                    "why": "Shows smooth 60 FPS live maps with vehicle paths at ZERO licensing cost.",
                    "where": "Central Tactical GIS map screen.",
                    "substitute": "Google Maps API / Mapbox.",
                    "why_not": "Google Maps charges per map load, costing cities Rs 4+ Lakhs/month. Leaflet is 100% free."
                }
            ]
        },
        {
            "cat_title": "2. AI VISION & EDGE VIDEO PROCESSING",
            "items": [
                {
                    "name": "YOLOv8-Nano",
                    "what": "Super-fast AI model for detecting vehicle number plates and car types.",
                    "why": "Runs extremely fast (45+ frames per second) even on low-cost hardware.",
                    "where": "Edge AI camera nodes on public buses and street poles.",
                    "substitute": "Faster R-CNN / SSD.",
                    "why_not": "Faster R-CNN is too slow (~10 FPS). SSD misses small or high-angle number plates."
                },
                {
                    "name": "PaddleOCR v4 + STN Dewarping",
                    "what": "AI text reader that automatically straightens crooked license plate photos.",
                    "why": "Reads English + Hindi plates with >93% accuracy, even from moving buses on bumpy roads.",
                    "where": "Edge camera software right after license plate detection.",
                    "substitute": "Tesseract OCR / EasyOCR.",
                    "why_not": "Tesseract is built for flat scanned paper; fails completely (<50%) on moving road photos."
                },
                {
                    "name": "NVIDIA Jetson + TensorRT (Edge AI)",
                    "what": "Compact, low-power AI mini-computer mounted inside buses and camera poles.",
                    "why": "Processes video right at the camera, saving Rs 50+ Lakhs/month in 4G data cost.",
                    "where": "Inside public buses (DTC/BMTC) and CCTV poles.",
                    "substitute": "Raspberry Pi / Cloud Video Streaming.",
                    "why_not": "Raspberry Pi lacks AI hardware (drops to 3 FPS). Cloud video streaming wastes huge 4G bandwidth."
                }
            ]
        },
        {
            "cat_title": "3. TRACKING & TRAJECTORY AI",
            "items": [
                {
                    "name": "ByteTrack + FastReID Engine",
                    "what": "AI that follows vehicles across video frames and matches car colors/shapes.",
                    "why": "Keeps tracking wanted cars even if the number plate is dirty, hidden, or unreadable.",
                    "where": "Bus cameras (local tracking) and Cloud engine (tracking across camera blind spots).",
                    "substitute": "DeepSORT.",
                    "why_not": "DeepSORT overworks the computer on every single frame, causing lag on camera hardware."
                },
                {
                    "name": "Hidden Markov Model (HMM) Map Matching",
                    "what": "Smart math algorithm that connects camera sightings along real road maps.",
                    "why": "Predicts a fleeing vehicle's exact route so police can set up roadblocks ahead.",
                    "where": "Cloud server whenever a wanted vehicle is spotted.",
                    "substitute": "Straight-line drawing / Deep Learning AI (LSTMs).",
                    "why_not": "Straight lines ignore roads (predicting driving through lakes/buildings). Deep AI gives unpredictable guesswork."
                }
            ]
        },
        {
            "cat_title": "4. BACKEND & DATA INFRASTRUCTURE",
            "items": [
                {
                    "name": "FastAPI & Node.js Express",
                    "what": "Fast asynchronous web server software.",
                    "why": "Handles thousands of camera pings per second and streams live map data smoothly.",
                    "where": "Main cloud backend servers.",
                    "substitute": "Django / Flask.",
                    "why_not": "Django and Flask block server threads, freezing under heavy camera traffic."
                },
                {
                    "name": "Redis In-Memory Database",
                    "what": "Super-fast memory database that checks plates instantly.",
                    "why": "Checks detected plates against police wanted lists in under 10 milliseconds.",
                    "where": "Cloud server hotlist cache & instant alert dispatcher.",
                    "substitute": "Standard SQL Database (PostgreSQL).",
                    "why_not": "Standard SQL databases read from hard drives, taking 50-100ms and creating alert delays."
                },
                {
                    "name": "SQLite (Store & Forward)",
                    "what": "Lightweight offline database stored directly inside the edge computer.",
                    "why": "Saves sightings when buses pass through tunnels/dead zones and auto-syncs when back online.",
                    "where": "Inside each bus and CCTV pole edge hardware.",
                    "substitute": "Temporary JSON text files.",
                    "why_not": "Text files corrupt easily when a bus engine shuts off unexpectedly. SQLite prevents data loss."
                }
            ]
        },
        {
            "cat_title": "5. INTEGRATION & LEGAL COMPLIANCE",
            "items": [
                {
                    "name": "MoRTH AIS-140 Bus Telemetry Standard",
                    "what": "Govt of India mandatory standard for public bus GPS and emergency hardware.",
                    "why": "Lets VESPER plug directly into existing public buses with ZERO extra hardware cost.",
                    "where": "Public bus fleet integration (DTC, BMTC, BEST).",
                    "substitute": "Custom hardware wiring.",
                    "why_not": "Installing custom hardware on 10,000 buses costs tens of crores. AIS-140 is already installed."
                },
                {
                    "name": "BSA Sec 63 SHA-256 & DPDP Act Face-Blurring",
                    "what": "Digital signature for legal evidence + automatic face blurring for citizen privacy.",
                    "why": "Makes photos 100% admissible in court while protecting pedestrian privacy automatically.",
                    "where": "On edge camera nodes before photos are saved or sent.",
                    "substitute": "Plain unhashed JPEG photos.",
                    "why_not": "Plain photos can be rejected in court as tampered; manual face blurring takes too much human time."
                }
            ]
        }
    ]

    for cat in categories:
        story.append(Paragraph(cat['cat_title'], cat_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=COLOR_ORANGE, spaceBefore=1, spaceAfter=6))

        for item in cat['items']:
            item_html = (
                f"<b>• What is it?</b> {item['what']}<br/>"
                f"<b>• Why is it used?</b> {item['why']}<br/>"
                f"<b>• Where is it used in VESPER?</b> {item['where']}<br/>"
                f"<b>• Substitute:</b> {item['substitute']}<br/>"
                f"<font color='#C53030'><b>• Why substitute was NOT used:</b> {item['why_not']}</font>"
            )

            box_table = Table([[
                Paragraph(f"<b>{item['name']}</b>", card_title_style),
            ], [
                Paragraph(item_html, card_body_style)
            ]], colWidths=[504])

            box_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
                ('BACKGROUND', (0,1), (-1,1), COLOR_LIGHT_BG),
                ('BOX', (0,0), (-1,-1), 0.75, COLOR_BORDER),
                ('PADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,0), 2),
            ]))

            story.append(KeepTogether([box_table, Spacer(1, 6)]))

    doc.build(story, canvasmaker=SimpleNumberedCanvas)
    print(f"Simple PDF generated at: {pdf_path}")

    # Copy to Downloads
    user_downloads = os.path.expanduser(r"~\Downloads")
    dest_path = os.path.join(user_downloads, filename)
    shutil.copy(pdf_path, dest_path)
    print(f"Copied to Downloads: {dest_path}")

if __name__ == "__main__":
    build_simple_pdf()
