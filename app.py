import streamlit as st
from itinerary import generate_itineraries
from image_fetcher import fetch_image

st.set_page_config(page_title="TripTactix: AI Trip Planner", layout="centered")
st.title("TripTactix")
st.subheader("Your AI-powered personal trip planner")

with st.form("trip_form"):
    destination = st.text_input("Destination", placeholder="e.g. Paris")
    num_days = st.number_input("Number of travel days", min_value=1, max_value=30, value=5)
    season_or_dates = st.text_input("Season or travel dates", placeholder="e.g. Summer, June 10-15")
    people = st.text_area(
        "Who's going? (number, ages, relationships)",
        placeholder="e.g. 2 adults (30, 32), 1 child (5)"
    )
    interests = st.text_input("Interests", placeholder="e.g. art, food, hiking, museums")
    submitted = st.form_submit_button("Generate Itineraries")

if submitted:
    user_input = {
        "destination": destination,
        "num_days": num_days,
        "season_or_dates": season_or_dates,
        "people": people,
        "interests": interests,
    }
    st.info("Generating personalized itinerary...")
    itineraries = generate_itineraries(user_input)
    st.write("\n---\n")
    st.header("Your Itinerary")
    # Always show the raw backend response for debugging
    st.subheader("Debug: Raw Backend Response")
    st.code(str(itineraries), language="json")
    if isinstance(itineraries, dict) and 'error' in itineraries:
        st.error(itineraries['error'])
        if 'raw_output' in itineraries:
            st.subheader("Raw AI Output")
            st.code(itineraries['raw_output'], language="json")
    elif isinstance(itineraries, dict) and 'title' in itineraries and 'days' in itineraries:
        st.subheader(itineraries.get("title", "Itinerary"))
        for day in itineraries.get("days", []):
            day_num = day.get('day', '?')
            activities = day.get('activities', [])
            if isinstance(activities, str):
                activities = [activities]
            st.markdown(f"**Day {day_num}:**")
            for activity in activities:
                image_data = fetch_image(activity)
                if isinstance(image_data, dict) and 'image_url' in image_data:
                    # Display image with attribution
                    st.image(image_data['image_url'], caption=activity, use_container_width=True)
                    st.markdown(f"- {activity}")
                    # Show photographer attribution
                    photographer = image_data.get('photographer', 'Unknown')
                    profile = image_data.get('profile', '#')
                    st.caption(f"📸 Photo by [{photographer}]({profile}) on Pexels")
                else:
                    # Fallback for string URLs or errors
                    st.image(image_data, caption=activity, use_container_width=True)
                    st.markdown(f"- {activity}")
            st.write(day.get("description", ""))
    else:
        st.warning("No valid itinerary generated. Please check your API key, try again, or see the debug output above.")
else:
    st.write("\n---\n")
    st.header("Your Itinerary")
    st.write("Fill out the form and click 'Generate Itineraries' to see your personalized trip plan!") 