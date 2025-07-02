# report.py
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4


def generate_reportlab_pdf(dfs_dict, chart_images_dict=None):
    """
    Generates a PDF report from a dictionary of pandas DataFrames and optional chart images
    using ReportLab. Each DataFrame will be summarized by its top 5 unique values per column.
    Chart images will be embedded if provided, appearing after the data tables.

    Args:
        dfs_dict (dict): A dictionary where keys are file names (str) and values are pandas DataFrames.
        chart_images_dict (dict, optional): A dictionary where keys are chart titles (str)
                                            and values are BytesIO objects containing image data (e.g., PNG).
                                            Defaults to None.
    Returns:
        io.BytesIO: A BytesIO object containing the generated PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define custom styles for a minimal and aesthetic look
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['h1'],
        fontSize=24,
        spaceAfter=24,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )

    section_header_style = ParagraphStyle(
        'SectionHeaderStyle',
        parent=styles['h2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=12,
        alignment=0,  # Left alignment
        textColor=colors.black
    )

    file_subheader_style = ParagraphStyle(
        'FileSubheaderStyle',
        parent=styles['h3'],
        fontSize=14,
        spaceBefore=10,
        spaceAfter=8,
        alignment=0,  # Left alignment
        textColor=colors.darkgrey
    )

    chart_title_style = ParagraphStyle(
        'ChartTitleStyle',
        parent=styles['h4'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=5,
        alignment=1,  # Center alignment
        textColor=colors.black
    )

    normal_text_style = styles['Normal']
    normal_text_style.fontSize = 10
    normal_text_style.leading = 12  # Line spacing

    story = []

    # Add a main title to the report
    story.append(Paragraph("Data Analysis Report", title_style))
    story.append(Spacer(1, 0.2 * inch))

    if not dfs_dict and not chart_images_dict:
        story.append(Paragraph("No data or charts available for reporting.", normal_text_style))
    else:
        # --- Add Data Tables Section ---
        if dfs_dict:
            story.append(Paragraph("Data Summaries (Top 5 Unique Values)", section_header_style))
            story.append(Spacer(1, 0.1 * inch))

            for file_name, df in dfs_dict.items():
                story.append(Paragraph(f"Summary for: {file_name}", file_subheader_style))
                story.append(Spacer(1, 0.1 * inch))

                # Prepare data for the unique values table
                unique_values_data = [["Column Name", "Top 5 Unique Values"]]
                for col in df.columns:
                    # Get top 5 unique values, convert to string for display
                    top_values = df[col].value_counts().head(5).index.tolist()
                    unique_values_data.append([col, ", ".join(map(str, top_values))])

                # Create the table for unique values
                table = Table(unique_values_data)

                # Apply a minimal table style
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align all text to left
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Header padding
                    ('FONTSIZE', (0, 0), (-1, -1), 9),  # Smaller font for data
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Light grid borders
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align content to top for multi-line cells
                ]))

                # Set column widths for the unique values table
                # Adjust these percentages based on expected content length
                col_widths = [doc.width * 0.3, doc.width * 0.7]  # 30% for column name, 70% for values
                table._argW = col_widths

                story.append(table)
                story.append(Spacer(1, 0.3 * inch))  # Space after each table

        # --- Add Visualizations Section (after tables) ---
        if chart_images_dict:
            story.append(Paragraph("Visualizations", section_header_style))
            story.append(Spacer(1, 0.1 * inch))

            # Iterate through charts and add each as a separate section
            for chart_title, img_buffer in chart_images_dict.items():
                story.append(Paragraph(chart_title, chart_title_style))
                story.append(Spacer(1, 0.05 * inch))  # Small space before image

                # Ensure the image buffer is at the beginning
                img_buffer.seek(0)

                # Create an Image flowable. Adjust width/height to fit page and maintain aspect ratio.
                # A common approach is to set width and let height scale proportionally.
                # Max width for letter page is around 7.5 inches (8.5 - 1 inch margins)
                img = Image(img_buffer, width=6.5 * inch)  # Set a fixed width
                # Calculate aspect ratio and set height
                # original_width, original_height = img.drawWidth, img.drawHeight # This doesn't work before draw
                # A more robust way would be to get image dimensions from the buffer if needed
                # For simplicity, we'll let ReportLab scale height proportionally if only width is given.

                story.append(img)
                story.append(Spacer(1, 0.2 * inch))  # Space after each chart

    doc.build(story)
    buffer.seek(0)  # Rewind the buffer to the beginning
    return buffer

