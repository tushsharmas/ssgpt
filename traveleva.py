import streamlit as st
import sqlite3
import json
import pyperclip
import os
import html
from datetime import datetime
from typing import List, Dict, Any
import requests
import time

# Configure page
st.set_page_config(
    page_title="TravelEva - Your AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup for history feature
DB_PATH = "traveleva_history.db"

def init_database():
    """Initialize SQLite database for storing question-answer history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rating INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def save_to_history(question: str, answer: str, category: str = "General"):
    """Save question-answer pair to history database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Keep only last 10 entries to avoid database bloat
        cursor.execute('''
            DELETE FROM qa_history 
            WHERE id NOT IN (
                SELECT id FROM qa_history 
                ORDER BY timestamp DESC 
                LIMIT 9
            )
        ''')
        
        cursor.execute('''
            INSERT INTO qa_history (question, answer, category)
            VALUES (?, ?, ?)
        ''', (question, answer, category))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving to history: {e}")
        return False

def get_history(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve question-answer history from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM qa_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        st.error(f"Error retrieving history: {e}")
        return []

def copy_to_clipboard(text: str, label: str = "text"):
    """Copy text to clipboard with user feedback"""
    try:
        pyperclip.copy(text)
        st.success(f"✅ {label} copied to clipboard!")
        return True
    except Exception as e:
        st.error(f"❌ Failed to copy to clipboard: {e}")
        # Fallback: show text in a text area for manual copying
        st.text_area(f"Copy this {label} manually:", value=text, height=100)
        return False

def create_copy_button(text: str, label: str, key: str):
    """Create a copy button with unique key"""
    if st.button(f"📋 Copy {label}", key=key, help=f"Copy {label} to clipboard"):
        copy_to_clipboard(text, label)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 300;
    }
    .question-container {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 6px solid #1976d2;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 1.1rem;
        color: #1565c0;
        font-weight: 500;
    }
    .answer-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #28a745;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        font-size: 1.05rem;
        line-height: 1.6;
        color: #212529;
    }
    .answer-text {
        color: #2c3e50;
        font-size: 1.1rem;
        line-height: 1.7;
        margin-top: 1rem;
    }
    .history-item {
        background-color: #fff3cd;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border-left: 5px solid #ffc107;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .history-item:hover {
        background-color: #fff8e1;
        transform: translateX(8px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .history-question {
        color: #856404;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    .history-answer {
        color: #6c757d;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .category-badge {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-right: 0.8rem;
        margin-bottom: 0.8rem;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .copy-button {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 0.7rem 1.2rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
        box-shadow: 0 3px 10px rgba(40, 167, 69, 0.3);
        transition: all 0.3s ease;
    }
    .copy-button:hover {
        background: linear-gradient(45deg, #218838, #1ea085);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
    }
    .stButton > button {
        background: linear-gradient(45deg, #007bff, #0056b3) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 3px 10px rgba(0, 123, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #0056b3, #004085) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4) !important;
    }
    .travel-categories {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    .category-chip {
        background: linear-gradient(45deg, #e3f2fd, #bbdefb);
        color: #1565c0;
        padding: 0.7rem 1.2rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #90caf9;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2);
    }
    .category-chip:hover {
        background: linear-gradient(45deg, #1976d2, #1565c0);
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(25, 118, 210, 0.4);
    }
    
    /* Improve overall text visibility */
    .stMarkdown {
        color: #2c3e50 !important;
    }
    
    .stTextArea textarea {
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        color: #2c3e50 !important;
    }
    
    .stSelectbox label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
    }
    
    .stExpander {
        border: 2px solid #e9ecef !important;
        border-radius: 10px !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Success and error message styling */
    .stSuccess {
        background-color: #d4edda !important;
        border: 1px solid #c3e6cb !important;
        color: #155724 !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        border: 1px solid #f5c6cb !important;
        color: #721c24 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

def get_travel_answer(question: str, category: str = "General") -> str:
    """Generate travel-related answers based on the question and category"""
    
    # Travel knowledge base with comprehensive answers
    travel_knowledge = {
        "flights": {
            "keywords": ["flight", "airline", "airport", "booking", "ticket", "plane", "aviation"],
            "responses": {
                "booking": "For flight booking, I recommend comparing prices on multiple platforms like Google Flights, Kayak, Expedia, and directly on airline websites. Book 6-8 weeks in advance for domestic flights and 2-3 months for international flights. Consider flexible dates and nearby airports for better deals.",
                "baggage": "Most airlines allow one carry-on bag (22x14x9 inches) and one personal item for free. Checked baggage fees vary by airline and destination. Pack essentials in carry-on, follow TSA liquid rules (3-1-1), and check airline-specific restrictions.",
                "delays": "Flight delays can be caused by weather, air traffic, mechanical issues, or crew scheduling. Know your rights: EU261 compensation in Europe, and various protections in other regions. Always have travel insurance and keep important items in carry-on."
            }
        },
        "accommodation": {
            "keywords": ["hotel", "hostel", "airbnb", "booking", "stay", "accommodation", "lodge"],
            "responses": {
                "booking": "Compare prices on Booking.com, Hotels.com, Airbnb, and direct hotel websites. Read recent reviews, check cancellation policies, and consider location vs. price. Book refundable rates when possible for flexibility.",
                "safety": "Research neighborhood safety, read recent guest reviews, verify property legitimacy, and check for security features like 24/7 front desk, secure entry, and in-room safes. Trust your instincts when arriving.",
                "amenities": "Essential amenities to consider: WiFi, air conditioning/heating, private bathroom, kitchen facilities (for longer stays), parking, and proximity to public transportation or attractions."
            }
        },
        "destinations": {
            "keywords": ["destination", "country", "city", "place", "visit", "travel to", "where"],
            "responses": {
                "europe": "Europe offers diverse experiences: Paris for romance and culture, Rome for history, Amsterdam for canals and museums, Barcelona for architecture and beaches, London for royal heritage, and Prague for medieval charm. Consider the Eurail pass for multi-country trips.",
                "asia": "Asia provides incredible diversity: Japan for culture and technology, Thailand for beaches and temples, India for spirituality and cuisine, China for history and modern cities, Vietnam for natural beauty and food, and Singapore for urban sophistication.",
                "americas": "The Americas offer vast experiences: USA for national parks and cities, Canada for nature and multiculturalism, Mexico for beaches and culture, Brazil for Amazon and Rio, Peru for Machu Picchu, and Argentina for wine and tango."
            }
        },
        "planning": {
            "keywords": ["plan", "itinerary", "budget", "preparation", "checklist", "organize"],
            "responses": {
                "budget": "Create a travel budget including: flights (30-40%), accommodation (25-35%), food (15-25%), activities (10-15%), and miscellaneous (10%). Use apps like Trail Wallet or Trabee Pocket to track expenses. Consider travel rewards credit cards.",
                "itinerary": "Plan your itinerary with flexibility: research must-see attractions, book accommodations in advance, leave room for spontaneous activities, consider travel time between locations, and have backup plans for weather-dependent activities.",
                "documents": "Essential travel documents: valid passport (6+ months validity), visa if required, travel insurance, copies of important documents, vaccination certificates, driver's license for car rentals, and emergency contact information."
            }
        },
        "safety": {
            "keywords": ["safety", "security", "danger", "crime", "health", "emergency"],
            "responses": {
                "general": "Travel safety tips: research destination safety, register with your embassy, keep copies of documents, use hotel safes, avoid displaying valuables, trust your instincts, stay connected with family, and have emergency contacts readily available.",
                "health": "Health precautions: consult a travel doctor 4-6 weeks before departure, get required vaccinations, pack a first-aid kit, bring prescription medications with extra supply, research local healthcare, and consider travel health insurance.",
                "scams": "Common travel scams to avoid: fake police checkpoints, overcharging tourists, fake travel agencies, pickpocketing in crowded areas, ATM skimming, and too-good-to-be-true deals. Research common scams for your specific destination."
            }
        }
    }
    
    question_lower = question.lower()
    
    # Determine category and find relevant response
    for cat, data in travel_knowledge.items():
        if any(keyword in question_lower for keyword in data["keywords"]):
            category = cat.title()
            
            # Find the most relevant response
            for response_key, response_text in data["responses"].items():
                if response_key in question_lower or any(word in question_lower for word in response_key.split()):
                    return response_text
            
            # Return first response if no specific match
            return list(data["responses"].values())[0]
    
    # Default responses for common travel questions
    default_responses = {
        "best time": "The best time to travel depends on your destination and preferences. Generally, shoulder seasons (spring and fall) offer good weather with fewer crowds and better prices. Research your specific destination's climate, peak seasons, and local events.",
        "what to pack": "Pack essentials based on your destination's climate and activities. Universal items: comfortable walking shoes, weather-appropriate clothing, toiletries, medications, chargers, travel documents, and a day pack. Pack light and leave room for souvenirs.",
        "travel insurance": "Travel insurance is highly recommended and covers trip cancellation, medical emergencies, lost luggage, and other unforeseen circumstances. Compare policies from companies like World Nomads, Allianz, or your credit card's travel benefits.",
        "currency": "Research your destination's currency and exchange rates. Use ATMs for better rates than currency exchange counters. Notify your bank of travel plans, carry some cash for small vendors, and consider a travel-friendly credit card with no foreign transaction fees.",
        "language": "Learn basic phrases in the local language: hello, thank you, please, excuse me, where is, how much, and numbers. Download translation apps like Google Translate with offline capabilities. Many tourist areas have English speakers.",
        "transportation": "Research local transportation options: public transit, taxis, ride-sharing, car rentals, or walking. Many cities offer tourist transport passes. Consider downloading local transport apps and maps for offline use."
    }
    
    # Check for default responses
    for key, response in default_responses.items():
        if key in question_lower:
            return response
    
    # Generic travel advice if no specific match
    return f"That's a great travel question! While I don't have specific information about '{question}', I recommend researching official tourism websites, reading recent traveler reviews, consulting travel guides like Lonely Planet or Rick Steves, and checking government travel advisories for the most current and accurate information. Feel free to ask me about flights, accommodations, destinations, planning, or safety - I have detailed knowledge in these areas!"

def display_history_sidebar():
    """Display history in sidebar"""
    with st.sidebar:
        st.header("📚 Recent Questions")
        
        history = get_history()
        
        if history:
            for i, item in enumerate(history):
                escaped_question_short = html.escape(item['question'][:45])
                escaped_question_full = html.escape(item['question'])
                escaped_answer = html.escape(item['answer'][:300])
                escaped_category = html.escape(item['category'])
                escaped_timestamp = html.escape(str(item['timestamp']))
                
                with st.expander(f"Q{i+1}: {escaped_question_short}{'...' if len(item['question']) > 45 else ''}", expanded=False):
                    # Enhanced display with better formatting
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                        <p><strong style="color: #495057;">📂 Category:</strong> 
                           <span style="background-color: #e9ecef; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.9rem;">
                               {escaped_category}
                           </span>
                        </p>
                        <p><strong style="color: #495057;">📅 Asked:</strong> 
                           <span style="color: #6c757d; font-size: 0.9rem;">{escaped_timestamp}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #1976d2;">
                        <strong style="color: #1565c0; font-size: 1rem;">❓ Question:</strong><br>
                        <div style="color: #1976d2; font-size: 1rem; margin-top: 0.5rem; line-height: 1.4;">
                            {escaped_question_full}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background-color: #f1f8e9; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #4caf50;">
                        <strong style="color: #2e7d32; font-size: 1rem;">🤖 Answer:</strong><br>
                        <div style="color: #388e3c; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                            {escaped_answer}{'...' if len(item['answer']) > 300 else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Copy buttons for history items
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📋 Copy Q", key=f"copy_q_{item['id']}", help="Copy question"):
                            copy_to_clipboard(item['question'], "Question")
                    with col2:
                        if st.button("📋 Copy A", key=f"copy_a_{item['id']}", help="Copy answer"):
                            copy_to_clipboard(item['answer'], "Answer")
                    with col3:
                        if st.button("🔄 Ask Again", key=f"ask_again_{item['id']}", help="Load this question"):
                            st.session_state.selected_question = item['question']
                            st.session_state.selected_category = item['category']
                            st.rerun()
        else:
            st.info("No questions asked yet. Start by asking a travel question!")
        
        # Clear history button
        if st.button("🗑️ Clear History", help="Clear all history"):
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM qa_history")
                conn.commit()
                conn.close()
                st.success("History cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing history: {e}")

def main():
    # Initialize database
    init_database()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>✈️ TravelEva - Your AI Travel Assistant</h1>
        <p>Get expert travel advice, tips, and recommendations for your next adventure!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display history sidebar
    display_history_sidebar()
    
    # Travel categories
    st.markdown("### 🗺️ Popular Travel Topics")
    st.markdown("""
    <div class="travel-categories">
        <div class="category-chip">✈️ Flights & Airlines</div>
        <div class="category-chip">🏨 Hotels & Accommodation</div>
        <div class="category-chip">🌍 Destinations</div>
        <div class="category-chip">📋 Trip Planning</div>
        <div class="category-chip">🛡️ Travel Safety</div>
        <div class="category-chip">💰 Budget Travel</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main question input
    st.markdown("### 💬 Ask Your Travel Question")
    
    # Check if a question was selected from history
    if 'selected_question' in st.session_state:
        default_question = st.session_state.selected_question
        default_category = st.session_state.get('selected_category', 'General')
        # Clear the session state
        del st.session_state.selected_question
        if 'selected_category' in st.session_state:
            del st.session_state.selected_category
    else:
        default_question = ""
        default_category = "General"
    
    # Question input
    question = st.text_area(
        "What would you like to know about travel?",
        value=default_question,
        height=100,
        placeholder="e.g., What's the best time to visit Japan? How do I find cheap flights? What should I pack for Europe?"
    )
    
    # Category selection
    categories = ["General", "Flights", "Accommodation", "Destinations", "Planning", "Safety", "Budget"]
    selected_category = st.selectbox("Category", categories, index=categories.index(default_category))
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Travel Advice", type="primary", use_container_width=True):
            if question.strip():
                with st.spinner("🤔 Thinking about your travel question..."):
                    # Simulate processing time
                    time.sleep(1)
                    
                    # Get answer
                    answer = get_travel_answer(question, selected_category)
                    
                    # Save to history
                    save_to_history(question, answer, selected_category)
                    
                    # Display question and answer
                    st.markdown("---")
                    
                    # Question display
                    escaped_question = html.escape(question)
                    st.markdown(f"""
                    <div class="question-container">
                        <span class="category-badge">{selected_category}</span>
                        <strong style="font-size: 1.2rem; color: #1565c0;">❓ Your Question:</strong><br><br>
                        <div style="font-size: 1.1rem; color: #1976d2; font-weight: 500; line-height: 1.5;">
                            {escaped_question}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Answer display with copy button
                    escaped_answer = html.escape(answer)
                    st.markdown(f"""
                    <div class="answer-container">
                        <strong style="font-size: 1.3rem; color: #28a745; margin-bottom: 1rem; display: block;">
                            🤖 TravelEva's Answer:
                        </strong>
                        <div class="answer-text">
                            {escaped_answer}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Copy buttons
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        create_copy_button(question, "Question", f"copy_current_q_{hash(question)}")
                    with col2:
                        create_copy_button(answer, "Answer", f"copy_current_a_{hash(answer)}")
                    with col3:
                        create_copy_button(f"Q: {question}\n\nA: {answer}", "Q&A Pair", f"copy_qa_{hash(question + answer)}")
                    
                    # Feedback
                    st.markdown("---")
                    st.markdown("### 📝 Was this helpful?")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("👍 Very Helpful"):
                            st.success("Thank you for your feedback!")
                    with col2:
                        if st.button("👌 Somewhat Helpful"):
                            st.info("Thanks! I'll try to improve.")
                    with col3:
                        if st.button("👎 Not Helpful"):
                            st.warning("Sorry about that. Please try rephrasing your question.")
            else:
                st.warning("Please enter a travel question!")
    
    # Sample questions
    st.markdown("---")
    st.markdown("### 💡 Sample Questions to Get You Started")
    
    sample_questions = [
        "What's the best time to visit Europe?",
        "How can I find cheap flights?",
        "What should I pack for a beach vacation?",
        "Is travel insurance worth it?",
        "How do I stay safe while traveling solo?",
        "What are the best travel apps?",
        "How much should I budget for a week in Thailand?",
        "What documents do I need for international travel?"
    ]
    
    cols = st.columns(2)
    for i, sample_q in enumerate(sample_questions):
        with cols[i % 2]:
            # Enhanced button styling with better visibility
            st.markdown(f"""
            <div style="margin: 0.5rem 0; padding: 0.2rem;">
                <div style="
                    background: linear-gradient(45deg, #17a2b8, #138496);
                    color: white;
                    padding: 1rem;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(23, 162, 184, 0.3);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    font-size: 1rem;
                    font-weight: 500;
                    line-height: 1.4;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">
                    💭 {sample_q}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Ask: {sample_q[:30]}...", key=f"sample_{i}", help=sample_q):
                st.session_state.selected_question = sample_q
                st.session_state.selected_category = "General"
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>✈️ <strong>TravelEva</strong> - Your AI Travel Assistant</p>
        <p>Get personalized travel advice, tips, and recommendations for your next adventure!</p>
        <p><em>Remember: Always verify important travel information with official sources.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()