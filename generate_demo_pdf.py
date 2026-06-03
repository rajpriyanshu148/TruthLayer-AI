"""
Generates a sample PDF with realistic factual claims for testing TruthLayer AI.
Run: python generate_demo_pdf.py
Requires: pip install reportlab
"""
import sys

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_JUSTIFY
except ImportError:
    print("Installing reportlab...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "-q"])
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_JUSTIFY

OUTPUT_FILE = "sample_factcheck_document.pdf"

CONTENT = [
    ("TechWorld Global Report 2024", "h1"),
    ("Technology, Finance & AI Industry Overview", "h2"),
    ("", "spacer"),
    ("Executive Summary", "h2"),
    (
        "This report provides an overview of key developments across the global technology, "
        "artificial intelligence, and financial markets. The following analysis draws on publicly "
        "available data and industry benchmarks to present a factual picture of the current landscape.",
        "body",
    ),
    ("", "spacer"),
    ("1. Artificial Intelligence Market", "h2"),
    (
        "The global artificial intelligence market was valued at $142.3 billion in 2023 and is "
        "projected to reach $1.8 trillion by 2030, growing at a compound annual growth rate (CAGR) "
        "of 37.3%. OpenAI was founded in 2015 in San Francisco and released GPT-4 in March 2023. "
        "Google DeepMind was formed in April 2023 through the merger of Google Brain and DeepMind. "
        "The United States holds approximately 45% of global AI investment.",
        "body",
    ),
    ("", "spacer"),
    ("2. Semiconductor Industry", "h2"),
    (
        "NVIDIA's market capitalization exceeded $3 trillion in June 2024, making it the most "
        "valuable company in the world at that time. The company's H100 GPU sells for approximately "
        "$30,000 per unit. Taiwan produces over 90% of the world's most advanced semiconductor chips "
        "through TSMC, which was founded in 1987. Intel was founded in 1968 by Gordon Moore and "
        "Robert Noyce in Mountain View, California.",
        "body",
    ),
    ("", "spacer"),
    ("3. Electric Vehicle Sector", "h2"),
    (
        "Tesla delivered approximately 1.81 million vehicles in 2023, missing its 2 million target. "
        "The company was founded in 2003 by Elon Musk and Martin Eberhard. China's BYD surpassed "
        "Tesla in global EV sales in Q4 2023, shipping around 526,000 units that quarter. "
        "The global EV market share reached 18% of total new car sales in 2023.",
        "body",
    ),
    ("", "spacer"),
    ("4. Social Media & Big Tech", "h2"),
    (
        "Meta Platforms reported revenues of $134.9 billion in 2023, a 16% increase year-over-year. "
        "Facebook, launched in February 2004 by Mark Zuckerberg at Harvard University, now has "
        "approximately 3.07 billion monthly active users. Apple became the first company to reach a "
        "$1 trillion market cap in August 2018. Microsoft acquired LinkedIn for $26.2 billion in 2016.",
        "body",
    ),
    ("", "spacer"),
    ("5. Space & Aerospace", "h2"),
    (
        "SpaceX's Starship rocket stands 121 meters tall, making it the tallest rocket ever built. "
        "The company has launched over 200 Falcon 9 missions and successfully landed boosters more "
        "than 250 times. NASA's Artemis I mission launched in November 2022 and traveled to the Moon "
        "without a crew. The International Space Station has been continuously inhabited since "
        "November 2, 2000.",
        "body",
    ),
    ("", "spacer"),
    ("6. Global Economy & Finance", "h2"),
    (
        "The United States GDP was approximately $27.4 trillion in 2023, making it the world's largest "
        "economy. China's GDP was approximately $17.7 trillion in the same year. The US Federal Reserve "
        "raised interest rates 11 times between March 2022 and July 2023, bringing the federal funds "
        "rate to a 22-year high of 5.25-5.5%. Bitcoin reached an all-time high of approximately "
        "$73,000 in March 2024.",
        "body",
    ),
    ("", "spacer"),
    ("7. Healthcare & Biotech", "h2"),
    (
        "Ozempic (semaglutide), manufactured by Novo Nordisk, was originally approved by the FDA "
        "in December 2017 for type 2 diabetes treatment. Novo Nordisk became Europe's most valuable "
        "company in 2023. The global pharmaceutical market was valued at $1.48 trillion in 2022. "
        "mRNA vaccines were first approved for human use against COVID-19 in December 2020.",
        "body",
    ),
    ("", "spacer"),
    ("Disclaimer", "h2"),
    (
        "The figures in this report are drawn from various public sources and may contain "
        "inaccuracies. Readers are advised to verify all statistics independently before "
        "making business or investment decisions.",
        "body",
    ),
]


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    style_h1 = ParagraphStyle("H1", parent=styles["Title"], fontSize=22, spaceAfter=6)
    style_h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, spaceBefore=12, spaceAfter=4)
    style_body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=11, leading=16, alignment=TA_JUSTIFY, spaceAfter=8)

    story = []
    for text, tag in CONTENT:
        if tag == "spacer":
            story.append(Spacer(1, 0.3 * cm))
        elif tag == "h1":
            story.append(Paragraph(text, style_h1))
        elif tag == "h2":
            story.append(Paragraph(text, style_h2))
        else:
            story.append(Paragraph(text, style_body))

    doc.build(story)
    print(f"[OK] Demo PDF created: {OUTPUT_FILE}")
    print("     Upload this file to TruthLayer AI to test fact-checking.")


if __name__ == "__main__":
    build_pdf()
