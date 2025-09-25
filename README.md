# Animal Healthcare AI Agent

A web-based AI-powered application for managing pet profiles and getting healthcare advice through an interactive chat interface.

## Features

- **Pet Profile Management**: Create, edit, and delete pet profiles with details like name, type, age, breed, gender, and medical history.
- **AI Chat Interface**: Interact with an AI agent to get personalized healthcare advice for your pets.
- **Chat History**: View and manage conversation history for each pet.
- **Responsive Design**: Works on desktop and mobile devices with a clean, modern UI.
- **Dark Mode**: Toggle between light and dark themes.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **AI Integration**: Custom AI agent for healthcare advice

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-vet
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Create a Pet Profile**: Click "Add New Profile" in the left panel and fill in the pet details.
2. **Select a Profile**: Click on a pet profile to activate it for chatting.
3. **Chat with AI**: Type your questions about pet health in the chat box and get AI-powered responses.
4. **View History**: Check the right panel for chat history grouped by pet.
5. **Edit/Delete Profiles**: Use the buttons in each profile item to modify or remove profiles.

## Project Structure

- `app.py`: Main Flask application
- `agent.py`: AI agent logic for healthcare advice
- `templates/index.html`: Main web interface
- `pet_health.db`: SQLite database for storing profiles and chat history
- `requirements.txt`: Python dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
