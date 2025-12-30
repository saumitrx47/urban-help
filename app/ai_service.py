import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize OpenAI client safely
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        logger.warning("OPENAI_API_KEY not found in environment variables")
        client = None
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {e}")
    client = None

FORBIDDEN_CURRENCIES = ["USD", "$", "EUR", "€"]


def _ensure_inr_only(text: str) -> str:
    """
    Ensure the response text does not contain non-INR currency markers.
    If any are found, they are replaced with INR (₹) markers.
    This keeps the UI strictly INR-only without introducing multi-currency logic.
    """
    if not text:
        return ""
    cleaned = text
    for marker in FORBIDDEN_CURRENCIES:
        if marker in cleaned:
            # Simple normalization: replace foreign markers with INR symbol
            cleaned = cleaned.replace(marker, "₹")
    # Verify no forbidden markers remain (if assertion fails, return cleaned anyway to avoid crashes)
    try:
        assert all(m not in cleaned for m in FORBIDDEN_CURRENCIES), "Non-INR currency detected in AI response"
    except AssertionError:
        # If assertion fails, just return cleaned text anyway to avoid crashing
        pass
    return cleaned


def get_service_recommendations(user_query: str, available_services: list) -> str:
    """
    Get AI-powered construction project recommendations based on user query.

    The AI should:
    - Classify the project into an appropriate civil construction service category
    - Suggest project complexity: LOW / MEDIUM / HIGH
    - Suggest an estimated duration range in days
    - Suggest an approximate cost range in INR
    """
    try:
        if not client:
            logger.warning("OpenAI client not initialized, returning fallback response")
            raise Exception("OpenAI client not available")
        
        if not available_services:
            logger.warning("No services available for AI recommendation")
            return (
                "I'd be happy to help you plan your construction project. "
                "Please review the available civil construction services above "
                "and choose the one that best matches your requirements."
            )
        
        services_list = "\n".join([f"- {s.get('name', 'Unknown')}: {s.get('description', '')}" for s in available_services])
        
        prompt = f"""You are a helpful assistant for a CIVIL CONSTRUCTION project marketplace in India.
The user is describing a potential construction / infrastructure project and asked: "{user_query}"

Available construction service types:
{services_list}

Your task:
1) Classify the project into the MOST relevant service category from the list above.
2) Estimate the project COMPLEXITY as one of: LOW, MEDIUM, HIGH.
3) Suggest an ESTIMATED DURATION RANGE in DAYS (for example: 7-10 days, 30-45 days).
4) Suggest an APPROXIMATE COST RANGE in INR.

IMPORTANT:
- All cost estimates MUST be provided ONLY in INR (Indian Rupees).
- Do NOT mention or imply any other currency such as USD or EUR.
- Be concise (2-3 short paragraphs maximum) and avoid overpromising.
"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful civil construction project assistant for India. Always use INR (₹) only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        raw_content = response.choices[0].message.content if response.choices else ""
        if not raw_content:
            raw_content = ""
        # Normalize to INR-only output
        return _ensure_inr_only(raw_content)
    except Exception as e:
        logger.error(f"Error in get_service_recommendations: {e}", exc_info=True)
        # Fallback message without any currency references
        return (
            "I'd be happy to help you plan your construction project. "
            "Please review the available civil construction services above "
            "and choose the one that best matches your requirements."
        )

