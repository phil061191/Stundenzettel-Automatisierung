"""
OCR Processor Module
Handles Gemini API integration for text extraction from scanned documents
"""

import os
import json
import logging
from pathlib import Path
import google.generativeai as genai
from PIL import Image

logger = logging.getLogger(__name__)


class OCRProcessor:
    """Processes scanned documents using Google Gemini API"""
    
    def __init__(self, api_key):
        """Initialize OCR processor with Gemini API key"""
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("Valid Gemini API key required. Please check your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        logger.info("OCR Processor initialized with Gemini API")
        
        # Load prompt template
        template_path = Path(__file__).parent.parent / "templates" / "stundenzettel_prompt.txt"
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                self.prompt_template = f.read()
            logger.debug(f"Loaded prompt template from {template_path}")
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            self.prompt_template = """Analysiere diesen gescannten Stundenzettel und extrahiere folgende Informationen im JSON-Format:

{
  "name": "Vollständiger Name des Mitarbeiters",
  "datum": "DD.MM.YYYY",
  "startzeit": "HH:MM",
  "endzeit": "HH:MM",
  "pause_minuten": 30
}

Regeln:
- Wenn keine Pause angegeben ist, verwende 0
- Zeiten im 24-Stunden-Format
- Datum im deutschen Format
- Nur valide JSON ausgeben, keine Erklärungen
"""
    
    def process_image(self, image_path):
        """
        Process an image file and extract timesheet data
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Extracted data or None if processing failed
        """
        try:
            logger.info(f"Processing image: {image_path}")
            
            # Open and prepare image
            img = Image.open(image_path)
            logger.debug(f"Image loaded: {img.size}, {img.mode}")
            
            # Generate content using Gemini
            response = self.model.generate_content([self.prompt_template, img])
            logger.debug(f"Gemini API response: {response.text}")
            
            # Extract JSON from response
            data = self._extract_json(response.text)
            
            if data:
                logger.info(f"Successfully extracted data: {data}")
                return data
            else:
                logger.error("Failed to extract valid JSON from response")
                return None
                
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            return None
    
    def process_pdf(self, pdf_path):
        """
        Process a PDF file and extract timesheet data
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            dict: Extracted data or None if processing failed
        """
        try:
            from pdf2image import convert_from_path
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Convert first page of PDF to image
            images = convert_from_path(pdf_path, first_page=1, last_page=1)
            
            if not images:
                logger.error("No pages found in PDF")
                return None
            
            # Process the first page
            response = self.model.generate_content([self.prompt_template, images[0]])
            logger.debug(f"Gemini API response: {response.text}")
            
            # Extract JSON from response
            data = self._extract_json(response.text)
            
            if data:
                logger.info(f"Successfully extracted data: {data}")
                return data
            else:
                logger.error("Failed to extract valid JSON from response")
                return None
                
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            return None
    
    def _extract_json(self, text):
        """Extract and parse JSON from API response"""
        try:
            # Try to find JSON in the response
            text = text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            data = json.loads(text)
            
            # Validate required fields
            required_fields = ["name", "datum", "startzeit", "endzeit", "pause_minuten"]
            if not all(field in data for field in required_fields):
                logger.error(f"Missing required fields in extracted data: {data}")
                return None
            
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.debug(f"Raw text: {text}")
            return None
