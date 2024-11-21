# Jezebel
Coding my own Alexa




The application incorporates various functionalities, such as speech recognition, speech synthesis (text-to-speech), and integration with external APIs(with primary one being an older version of ChatGPT by OpenAI) to perform tasks like playing songs. The project incorporates a graphical user interface (GUI) developed using the tkinter library. The GUI includes buttons to start and stop listening for user commands. The user input and Jezibel's responses are displayed in separate labels within the GUI.



## Key Changes on version 0.6:
  1. Enhanced error handling to manage different exceptions more gracefully.
  2. Added basic logging for debugging and tracking issues.
  3. Added an option to toggle between single and continuous listening modes.
  4. Added more GUI elements for better user interaction and feedback.
  5. Added the ability to open websites and run simple system commands.

## Key Changes on version 0.7:
  1. Added "Weather Information Retrieval" feature
  2. Added "Reminder/Timer" functionality
  3. Added "News Headlines" feature
  4. Added "Joke Telling" feature
  5. Added "Text-to-Command Mapping for Common Tasks" so the application can perform local tasks
  6. Added Voice feedback toggle to allow users to toggle between Jezebel responding via text only or voice
#####  7. From this version on, 3 API keys will be reqiured: An OpenAI API key, an OpenWeatherMap API key, and a NewsAPI key
  8. Re-organized the core functionalities
  9. Added/improved exception handling; especially for external APIs and speech recognition errors.
  10. Added dynamic voice selection that provides an option to change the voice dynamically instead of hardcoding it

## Key Changes on version 0.8.0:
  1. Added "Weather Information Retrieval" feature
  2. Used python-dotenv to load API keys from a .env file, improving security
  3. Updated to use the ChatCompletion API with the GPT-3.5-turbo model, which is more advanced and cost-effective
  4. Increased timeout and phrase time limit for better user experience
  5. Implemented a more efficient command processing system using a dictionary of functions
  6. Improved error handling and logging throughout the code
  7. GUI improvements
  8. Implemented the play_song function using ytmusicapi
  9. Added a basic open_website function
  10. Included a placeholder for the run_command function (disabled for security reasons)
  11. Reorganized the code for better readability and maintainability

# Important notes:
- Make sure you have the required libraries installed before running the code.
- Preferably use a microphone for convenience.
- To use V 0.8 and above, you'll need to:
  1. Install additional dependencies: python-dotenv
  2. Create a .env file in the same directory as the script with your API keys
