# TripTactix 🧳✈️

**Your personal trip organizer!** Just tell him where, when, and who is traveling, and you'll get the perfect itinerary, with everything you need to read, see and know for the perfect trip.

## Problem/Opportunity

Planning a multi-day trip is time-consuming: travellers (including us) juggle countless blogs, maps, and social networks to build an agenda that fits ages, interests, and season. An AI that aggregates that research and turns simple preferences into ready-to-use daily plans (illustrated with real photos) saves tons of planning time and provide inspiration for the traveler.

## Core Flow (MVP)

### User Input
The user provides essential information:
- **Destination**
- **Number of travel days**
- **Dates or season**
- **Who's going** (number of people, ages, relationship)
- **Interests**

### AI Processing
1. **Generate** 2–3 unique itineraries using an LLM, customized based on user input
2. **Retrieve** relevant real-world photos for each activity or location
3. **Display** itineraries in an interactive Streamlit UI with:
   - Daily breakdowns
   - Activity descriptions
   - Photos
   - Save/share option
4. **Optionally** collect user feedback and regenerate with updates

## AI Pipeline

```
[API 1: Cohere]
    ➔ Generates trip itinerary (JSON-formatted)
    ↓
Structured Itinerary Data
    ↓
[API 2: Pexels Image Search API]
    ➔ Fetches relevant real-world images for each activity/location
    ↓
Itineraries with Activity Images
    ↓
[API 3: Hugging Face Inference API (Stable Diffusion)]
    ➔ Generates a custom summary image of the trip (based on destination, participants, and season)
    ↓
Final Enhanced Itinerary with AI-generated Trip Summary Image
    ↓
Streamlit UI
    ➔ Displays the generated summary image prominently at the top
    ➔ Renders detailed daily itineraries, each activity enriched with real images
```

## Features

- 🤖 **AI-Powered Itineraries**: Uses Cohere's Command R+ model to generate personalized travel plans
- 🖼️ **Real Images**: Fetches relevant images from Pexels for each activity
- 🎨 **Custom Trip Visualization**: AI-generated summary images using Stable Diffusion
- 📱 **Beautiful UI**: Clean Streamlit interface with responsive design
- 🎯 **Personalized**: Considers destination, travel dates, group info, and interests
- 📸 **Photo Attribution**: Properly credits photographers with links to their profiles

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/tomerfe/travel-itinerary-ai.git
cd travel-itinerary-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys
Create a `.env` file in the project root:
```bash
# Copy the example file
cp env.example .env

# Edit .env with your actual API keys
COHERE_API_KEY=your_cohere_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### 4. Get API Keys

#### Cohere API Key
1. Go to [https://cohere.ai/](https://cohere.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard

#### Pexels API Key
1. Go to [https://www.pexels.com/api/](https://www.pexels.com/api/)
2. Sign up for a free account
3. Get your API key

#### Hugging Face API Key
1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Sign up for a free account
3. Create a new token with "Read" access

### 5. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
travel-itinerary-ai/
├── app.py              # Main Streamlit application
├── itinerary.py        # AI itinerary generation logic
├── image_fetcher.py    # Pexels image fetching with attribution
├── requirements.txt    # Python dependencies
├── env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Usage

The app uses three main APIs:

1. **Cohere API**: For generating travel itineraries
2. **Pexels API**: For fetching relevant images
3. **Hugging Face API**: For generating custom trip summary images

All APIs offer free tiers suitable for personal use and development.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues:
1. Check that your API keys are correctly set in the `.env` file
2. Ensure all dependencies are installed
3. Open an issue on GitHub with details about the problem 