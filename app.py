import streamlit as st
from itinerary import generate_itineraries, generate_trip_summary_image
from image_fetcher import fetch_image
import io

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
    
    # Generate trip summary image with Hugging Face
    try:
        with st.spinner("Creating your trip summary image..."):
            trip_image = generate_trip_summary_image(user_input)
    except Exception as e:
        st.warning(f"Image generation failed: {str(e)}")
        trip_image = "https://via.placeholder.com/1024x768?text=Image+Generation+Failed"
    
    # Generate itinerary
    try:
        itineraries = generate_itineraries(user_input)
    except Exception as e:
        st.error(f"Itinerary generation failed: {str(e)}")
        itineraries = {"error": f"Exception during generation: {str(e)}"}
    
    st.write("\n---\n")
    st.header("Your Itinerary")
    
    # Display trip summary image
    st.subheader("🖼️ Your Trip Visualization")
    if isinstance(trip_image, io.BytesIO):
        st.image(trip_image, caption=f"AI-generated visualization of your trip to {destination}", use_container_width=True)
    else:
        # Fallback URL if image generation failed
        st.image(trip_image, caption=f"Your trip to {destination}", use_container_width=True)
    
    if isinstance(itineraries, dict) and 'error' in itineraries:
        st.error("Sorry, there was an issue generating your itinerary. Please try again.")
        # Show debug information
        with st.expander("Debug Information (click to expand)"):
            st.write("Error details:", itineraries.get('error', 'Unknown error'))
            if 'raw_output' in itineraries:
                st.write("Raw output:", itineraries['raw_output'])
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
        st.warning("No valid itinerary generated. Please try again.")
else:
    st.write("\n---\n")
    st.header("Your Itinerary")
    st.write("Fill out the form and click 'Generate Itineraries' to see your personalized trip plan!") 