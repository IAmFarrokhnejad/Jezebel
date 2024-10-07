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


# Important notes:
- Make sure you have the required libraries installed before running the code.
- Preferably use a microphone for convenience.
- Version 0.7 and above require 3 API keys. Check they "Key Changes" above. Previous versions only require the OpenAI API key.
