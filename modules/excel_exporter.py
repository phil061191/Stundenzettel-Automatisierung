"""
Excel Exporter Module
Handles Excel file creation with formatting
"""

import logging
from datetime import datetime
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

logger = logging.getLogger(__name__)


class ExcelExporter:
    """Exports timesheet data to formatted Excel files"""
    
    def __init__(self, output_folder):
        """Initialize Excel exporter with output folder"""
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.data_rows = []
        logger.info(f"Excel Exporter initialized with output folder: {output_folder}")
    
    def add_entry(self, data):
        """
        Add a timesheet entry
        
        Args:
            data: Dictionary with keys: name, datum, startzeit, endzeit, pause_minuten, netto_stunden
        """
        self.data_rows.append(data)
        logger.debug(f"Added entry: {data}")
    
    def export(self):
        """
        Export all entries to Excel file
        
        Returns:
            str: Path to created Excel file or None if failed
        """
        if not self.data_rows:
            logger.warning("No data to export")
            return None
        
        try:
            # Create workbook
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Stundenzettel"
            
            # Define headers
            headers = ["Name", "Datum", "Startzeit", "Endzeit", "Pause (Min)", "Netto-Stunden"]
            
            # Style definitions
            header_font = Font(bold=True, size=12)
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            border_side = Side(style='thin', color='000000')
            border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)
            
            # Write headers
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True, size=12, color="FFFFFF")
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = border
            
            # Sort data by date and name
            sorted_data = sorted(self.data_rows, key=lambda x: (
                self._parse_date(x.get('datum', '')),
                x.get('name', '')
            ))
            
            # Write data rows
            for row_num, entry in enumerate(sorted_data, 2):
                # Name
                ws.cell(row=row_num, column=1, value=entry.get('name', '')).border = border
                
                # Datum (convert to Excel date)
                datum_str = entry.get('datum', '')
                try:
                    datum_obj = datetime.strptime(datum_str, "%d.%m.%Y")
                    cell = ws.cell(row=row_num, column=2, value=datum_obj)
                    cell.number_format = 'DD.MM.YYYY'
                except:
                    cell = ws.cell(row=row_num, column=2, value=datum_str)
                cell.border = border
                
                # Startzeit
                ws.cell(row=row_num, column=3, value=entry.get('startzeit', '')).border = border
                
                # Endzeit
                ws.cell(row=row_num, column=4, value=entry.get('endzeit', '')).border = border
                
                # Pause
                ws.cell(row=row_num, column=5, value=entry.get('pause_minuten', 0)).border = border
                
                # Netto-Stunden
                cell = ws.cell(row=row_num, column=6, value=entry.get('netto_stunden', 0.0))
                cell.number_format = '0.00'
                cell.border = border
            
            # Auto-adjust column widths
            column_widths = {
                'A': 25,  # Name
                'B': 15,  # Datum
                'C': 12,  # Startzeit
                'D': 12,  # Endzeit
                'E': 15,  # Pause
                'F': 18   # Netto-Stunden
            }
            
            for col, width in column_widths.items():
                ws.column_dimensions[col].width = width
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"stundenzettel_export_{timestamp}.xlsx"
            filepath = self.output_folder / filename
            
            # Save workbook
            wb.save(filepath)
            logger.info(f"Excel file created: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            return None
    
    def clear_entries(self):
        """Clear all stored entries"""
        self.data_rows = []
        logger.debug("Cleared all entries")
    
    def _parse_date(self, date_str):
        """Parse date string for sorting"""
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except:
            return datetime.min
