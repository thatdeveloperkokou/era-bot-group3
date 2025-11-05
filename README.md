# 💡 Electricity Supply Logger Bot

A full-stack application for tracking power outages and electricity supply with a beautiful React frontend and Python Flask backend.

## Features

- 🔐 **User Authentication** - Secure login and registration
- 💬 **Chat Interface** - Log power events through a chat-like interface
- 📊 **Data Visualization** - Interactive charts showing daily/weekly/monthly statistics
- ⚡ **Real-time Logging** - Track when power comes on and goes off
- 📈 **Statistics** - View total light hours for day, week, or month
- 📋 **Report Command** - Type "report" in chat to get a brief summary of electricity data
- 📱 **Mobile Responsive** - Fully optimized for mobile devices with collapsible charts

## Project Structure

```
.
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── context/        # Auth context
│   │   ├── services/       # API service
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

### Testing the Backend

To verify the backend is running correctly, you can:

1. **Manual test**: Open `http://localhost:5000` in your browser. You should see a JSON response with API status.

2. **Use the test script** (optional):
```bash
cd backend
pip install requests  # Only needed for the test script
python test_backend.py
```

## Troubleshooting

### Backend returns 404 errors

If you're getting 404 errors from the backend:

1. **Check if the backend is running**:
   - Make sure you see "Starting Electricity Supply Logger API..." message
   - Verify the server is listening on `http://localhost:5000`

2. **Check the port**:
   - Make sure port 5000 is not being used by another application
   - You can change the port in `backend/app.py` if needed

3. **Verify CORS is enabled**:
   - The backend should have CORS enabled (already configured)
   - Check browser console for CORS errors

4. **Check API endpoint URLs**:
   - Frontend calls `http://localhost:5000/api/*`
   - Make sure the backend is accessible at that URL

5. **Common issues**:
   - **Firewall blocking**: Windows Firewall might block Python
   - **Port already in use**: Another app might be using port 5000
   - **Virtual environment**: Make sure you activated the virtual environment and installed dependencies

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Log Power Events**: 
   - Use the "Power ON" or "Power OFF" buttons
   - Or type "power on" / "power off" in the chat input
3. **View Statistics**: 
   - See total light hours in the statistics panel
   - Switch between Today, Week, and Month views
   - View detailed charts showing daily breakdown
   - On mobile: Click "Show Charts" button to toggle chart visibility
4. **Get Report**: 
   - Type "report" or "summary" in the chat to get a brief summary
   - Shows today's hours, week's hours, month's hours, and average daily hours

## Team Members

- Eklo Kokou Salomon
- Adedoyin Ebenezer
- Babalola Ridwan

## Technologies Used

- **Frontend**: React, React Router, Recharts, Axios
- **Backend**: Python, Flask, Flask-CORS, JWT
- **Data Storage**: CSV files (can be easily migrated to a database)

## API Endpoints

- `POST /api/register` - Register a new user
- `POST /api/login` - Login user
- `POST /api/log-power` - Log a power event (on/off)
- `GET /api/stats?period=week` - Get statistics (day/week/month)
- `GET /api/recent-events?limit=10` - Get recent power events

## Deployment

This project is configured for deployment on:
- **Frontend**: Vercel (React static hosting)
- **Backend**: Railway (Python Flask hosting)

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

### Quick Deployment Steps:

1. **Push to GitHub**: Follow the steps in DEPLOYMENT.md to push your code
2. **Deploy Backend to Railway**: 
   - Connect your GitHub repo
   - Set root directory to `backend`
   - Railway will auto-detect and deploy
3. **Deploy Frontend to Vercel**:
   - Connect your GitHub repo
   - Set root directory to `frontend`
   - Add environment variable: `REACT_APP_API_URL` = your Railway backend URL
   - Deploy!

## Notes

- The backend uses CSV files for data storage. For production, consider migrating to a database like SQLite or PostgreSQL.
- JWT tokens are stored in localStorage. For enhanced security, consider using httpOnly cookies.
- The secret key in `app.py` should be changed for production use (use environment variable `SECRET_KEY`).

