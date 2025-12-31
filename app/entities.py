import spacy
import dateparser
import re
from typing import Dict, List
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

TIME_DESCRIPTORS = {'morning', 'afternoon', 'evening', 'night', 'noon', 'midnight'}

CUSTOM_ENTITIES = {
    "time": [
        r"\b\d{1,2}:\d{2}\s?(am|pm)?\b",
        r"\b\d{1,2}\s?(am|pm)\b",
    ],
}

def normalize_time(time_str: str) -> str:
    """
    Convert time expressions to 24-hour format HH:MM
    """
    time_str = time_str.lower().strip()
    
    # Handle special cases
    if time_str == 'noon':
        return '12:00'
    if time_str == 'midnight':
        return '00:00'
    
    # Match patterns like: 7am, 2pm, 10:30am, 3:45 pm
    match = re.match(r'(\d{1,2})(?::(\d{2}))?\s?(am|pm)?', time_str)
    
    if not match:
        return time_str
    
    hour = int(match.group(1))
    minute = int(match.group(2)) if match.group(2) else 0
    period = match.group(3)
    
    # Convert to 24-hour format
    if period == 'pm' and hour != 12:
        hour += 12
    elif period == 'am' and hour == 12:
        hour = 0
    
    return f"{hour:02d}:{minute:02d}"

def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract entities using spaCy + dateparser for date resolution.
    Returns: { entity_type: [values] }
    """
    results: Dict[str, List[str]] = {}
    processed_spans = set()
    
    doc = nlp(text)
    
    # 1. Extract entities from spaCy
    for ent in doc.ents:
        entity_type = ent.label_.lower()
        
        # For DATE entities, extract embedded numbers as cardinals
        if entity_type == 'date':
            numbers = re.findall(r'\b(\d+)\b', ent.text)
            if numbers:
                if 'cardinal' not in results:
                    results['cardinal'] = []
                results['cardinal'].extend(numbers)
            
            # Resolve the date
            parsed_date = dateparser.parse(
                ent.text,
                settings={
                    'RELATIVE_BASE': datetime.now(),
                    'PREFER_DATES_FROM': 'future'
                }
            )
            value = parsed_date.strftime('%Y-%m-%d') if parsed_date else ent.text
        else:
            value = ent.text
        
        if entity_type not in results:
            results[entity_type] = []
        results[entity_type].append(value)
        processed_spans.add((ent.start_char, ent.end_char))
    
    # 2. Extract custom patterns
    for entity_type, patterns in CUSTOM_ENTITIES.items():
        matches = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                span = (match.start(), match.end())
                if not any(start <= span[0] < end or start < span[1] <= end 
                          for start, end in processed_spans):
                    match_text = match.group(0)
                    matches.append(match_text)
                    processed_spans.add(span)
        
        if matches:
            if entity_type not in results:
                results[entity_type] = []
            results[entity_type].extend(matches)
    
    # 3. Normalize times to 24-hour format
    if 'time' in results:
        results['time'] = [normalize_time(t) for t in results['time'] if t.lower() not in TIME_DESCRIPTORS]
    
    # 4. Deduplicate
    for key in results:
        results[key] = list(dict.fromkeys(results[key]))
    
    return results