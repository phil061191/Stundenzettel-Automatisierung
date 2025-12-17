"""
Time Calculator Module
Handles work time calculations with break logic
"""

import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TimeCalculator:
    """Calculates net working hours from timesheet data"""
    
    @staticmethod
    def calculate_net_hours(start_time, end_time, pause_minutes):
        """
        Calculate net working hours
        
        Args:
            start_time: Start time string (HH:MM)
            end_time: End time string (HH:MM)
            pause_minutes: Break time in minutes
            
        Returns:
            float: Net working hours (rounded to 2 decimals)
        """
        try:
            # Parse times
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            
            # Handle overnight shifts
            if end < start:
                end += timedelta(days=1)
            
            # Calculate total hours
            total_time = end - start
            total_minutes = total_time.total_seconds() / 60
            
            # Apply break logic: only subtract breaks > 30 minutes
            if pause_minutes > 30:
                total_minutes -= pause_minutes
                logger.debug(f"Break > 30 min: {pause_minutes} min deducted")
            else:
                logger.debug(f"Break <= 30 min: {pause_minutes} min NOT deducted")
            
            # Convert to hours
            net_hours = total_minutes / 60
            net_hours = round(net_hours, 2)
            
            logger.info(f"Calculated: {start_time} - {end_time}, Break: {pause_minutes}min = {net_hours}h")
            
            return net_hours
            
        except Exception as e:
            logger.error(f"Error calculating hours: {e}")
            return 0.0
    
    @staticmethod
    def validate_times(start_time, end_time):
        """
        Validate time format and logic
        
        Args:
            start_time: Start time string (HH:MM)
            end_time: End time string (HH:MM)
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            return True
        except ValueError:
            logger.error(f"Invalid time format: {start_time} - {end_time}")
            return False
    
    @staticmethod
    def format_time(time_str):
        """
        Format time string to HH:MM
        
        Args:
            time_str: Time string
            
        Returns:
            str: Formatted time (HH:MM)
        """
        try:
            time_obj = datetime.strptime(time_str, "%H:%M")
            return time_obj.strftime("%H:%M")
        except:
            return time_str
