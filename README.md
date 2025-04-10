# Smart Result System

A GUI application for managing student results, courses, and performance tracking with Firebase integration.

## Features

### Admin Dashboard
- User Management (Students, Teachers, Parents)
- Course & Subject Management
- Result Management
- Dashboard & Analytics
- System Settings

### Firebase Integration
- Real-time database for storing and retrieving data
- User authentication for secure access
- Cloud storage for student documents and images
- Real-time updates across multiple clients

### Display Options
- Full screen mode by default
- Toggle between full screen and windowed mode with buttons
- Press Escape key to exit full screen mode

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/smart_result_system.git
cd smart_result_system
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Firebase Setup:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Firestore Database and Authentication
   - Download your service account key file
   - Rename it to `firebase-credentials.json` and place it in the project root folder
   - For demo purposes, a sample credential file will be created automatically

## Usage

Run the application:
```
python main.py
```

The application will start in full screen mode. You can exit full screen mode by:
- Pressing the Escape key
- Clicking the "Exit Fullscreen" button
- Toggle back to full screen by clicking "Enter Fullscreen" button

## Login Credentials

For demonstration purposes, the following login credentials can be used:

- **Admin**:
  - Email: admin@smr.com
  - Password: admin123
  - Select "Admin" role

- **Teacher**:
  - Email: teacher@smr.com
  - Password: teacher123
  - Select "Teacher" role

## Real-Time Features

- Student data updates in real-time across all clients
- Changes made by one user are instantly visible to others
- Real-time notifications for important events

## Requirements

- Python 3.7 or higher
- Firebase Admin SDK
- CustomTkinter
- Other dependencies listed in requirements.txt

## License

[MIT](https://choosealicense.com/licenses/mit/) 