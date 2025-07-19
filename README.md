# TripTactix 🧳✈️

An AI-powered personal trip planner that generates personalized travel itineraries with real images.

## Features

- 🤖 **AI-Powered Itineraries**: Uses Cohere's Command R+ model to generate personalized travel plans
- 🖼️ **Real Images**: Fetches relevant images from Pexels for each activity
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

### 5. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Enter Trip Details**:
   - Destination (e.g., "Paris", "Tokyo")
   - Number of travel days (1-30)
   - Season or travel dates
   - Group information (ages, relationships)
   - Interests (e.g., "art, food, hiking, museums")

2. **Generate Itinerary**: Click "Generate Itineraries" to create your personalized travel plan

3. **View Results**: See your itinerary with daily activities, descriptions, and relevant images

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

## Features in Detail

### AI Itinerary Generation
- Uses Cohere's Command R+ model for natural language generation
- Generates structured JSON responses with daily activities
- Includes error handling and fallback responses
- Supports 1-30 day itineraries

### Image Integration
- Fetches relevant images from Pexels for each activity
- Proper photographer attribution with profile links
- Fallback images if API fails
- Optimized for landscape orientation

### User Interface
- Clean, responsive Streamlit interface
- Form validation and error handling
- Debug mode for troubleshooting
- Mobile-friendly design

## API Usage

The app uses two main APIs:

1. **Cohere API**: For generating travel itineraries
2. **Pexels API**: For fetching relevant images

Both APIs offer free tiers suitable for personal use and development.

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
3. Check the debug output in the app for error messages
4. Open an issue on GitHub with details about the problem

## Roadmap

- [ ] Add support for multiple itinerary options
- [ ] Integrate with more image APIs
- [ ] Add weather information
- [ ] Include restaurant recommendations
- [ ] Add export functionality (PDF, calendar)
- [ ] Mobile app version 