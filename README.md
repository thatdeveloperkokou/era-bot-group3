# Electricity Supply Logger Bot

**Live Site:** [https://era-bot-group3-nx3x.vercel.app/](https://era-bot-group3-nx3x.vercel.app/)

## 🚀 Quick Setup

### Email Configuration

See **[EMAIL_SETUP.md](./backend/EMAIL_SETUP.md)** for detailed email configuration instructions.

### 🗄️ Database Configuration

**The application now uses PostgreSQL for data storage!**

**Setup:**
- See **[POSTGRESQL_SETUP.md](./backend/POSTGRESQL_SETUP.md)** for detailed PostgreSQL setup instructions
- **Render (Recommended):** Add PostgreSQL database in Render dashboard (see [RENDER_MIGRATION.md](./RENDER_MIGRATION.md))
- **Railway (Alternative):** Add PostgreSQL database in Railway dashboard
- **Local Development:** Install PostgreSQL and configure connection
- **Migration:** Run `python backend/migrate_to_postgresql.py` to migrate existing data

**Benefits:**
- ✅ Data persists permanently
- ✅ Scalable and reliable
- ✅ Industry standard
- ✅ Better performance
- ✅ Built-in backups (on cloud providers)

**Quick summary:**
1. **Gmail (Recommended for Development):**
   - Enable 2FA on your Google account
   - Create an App Password: https://myaccount.google.com/apppasswords
   - Add credentials to `backend/.env`

2. **Other Options:** Outlook, Yahoo, SendGrid, Mailgun
   - See `backend/EMAIL_SETUP.md` for setup instructions

3. **Without email:** Verification codes will be printed to backend console (development only)

**Note:** ProtonMail does NOT support SMTP for regular accounts. Use Gmail, Outlook, or a transactional email service instead.

## The Problem

In many areas, electricity is unreliable. Without proper tracking, people don't really know:

• How many hours of power they actually get each day

• When and how often power goes off

• How to plan daily tasks around power availability

• How to hold utility companies(NEPA) accountable with real data

This app makes it easy for anyone to log, track, and analyze their electricity supply — all from their phone or computer.

## What the App Can Do

### User Authentication

• Register and log in securely

• Each user's data is private and separate

• Uses JWT (JSON Web Token) for secure access

## Power Logging process

• Tap "Power ON" or "Power OFF" buttons

• Or type natural commands like "power on", "power off", or "report"

• Every event is saved automatically with the date and time

## How Data is Visualized

• Interactive charts show your daily electricity hours

• View data by day, week, or month

• Clearly see patterns of when power is usually available or gone

## Statistics and Reports Given by the Bot

• Get total light hours for any time period

• See daily breakdowns of electricity usage

• Type "report" to get a quick summary of:
  - Today's total hours
  - Weekly and monthly averages
  - Last power event time

## Real-Time Updates

• Data refreshes automatically every 30 seconds

• Chat and charts update instantly when you log a new event

## How Our Bot Works

### 1. Authentication Flow

• User signs up or logs in

• Password is encrypted

• Backend sends a JWT token to the frontend

• Token is stored in the browser (localStorage)

• All future requests use the token for verification

### When the user logs "Power ON/OFF"

→ React frontend sends it to Flask API

→ Backend checks the token and records the event

→ Data is stored in a CSV file (with user ID, event type, and timestamp)

### How Statistics is Calculated

When a user requests stats,

→ Backend reads their CSV logs

→ Filters data for the requested time range

→ Calculates total power hours by pairing ON and OFF times

→ Sends back total hours, daily breakdowns, and averages

### Data Flow Summary

User → React Interface → Axios (API call) → Flask Backend → CSV File → Stats Engine → JSON Response → React UI

### How Report is Generated

Typing "report" gives:

• Total hours for today

• Weekly and monthly summaries

• Averages and recent events

## Tech Stack

### Frontend

• React for UI

• React Router for Navigation

• Recharts for Charts and graphs

• Axios for API calls

• CSS3 for Styling

### Backend

• Python and Flask 3.0 for logic and API server

• Flask-CORS to help communicate with our frontend

• PyJWT for Authentication tokens to store login data

• CSV files for Data storage

## Deployment

• Vercel for Frontend hosting

• Render for Backend hosting (migrated from Railway)

• PostgreSQL database on Render

• Cron jobs on Render for automated power logging

• GitHub to help with collaboration with my team members and Version control

**Render Setup**: See [RENDER_MIGRATION.md](./RENDER_MIGRATION.md) for complete guide to set up PostgreSQL database on Render.

## Why Our Project Matters

• Empowers people to understand their power supply.

• Helps users plan better and live smarter

• Provides real data for community and government accountability

• Easy to use, even for non-technical users

• Scalable and privacy-focused

## Future Enhancements

HERE ARE THINGS WE WISH TO DO IN THE FUTURE IF POSSIBLE

• Move data storage to a real database

• Add notifications when power changes

## Credits

**THIS PROJECT WAS MADE POSSIBLE BY THE DELEGATED STUDENTS OF GROUP 3 IN ENGINEER GONI'S EXPERT SYSTEM'S CLASS:**

1. Eklo Kokou Salomon
2. Adedoyin Ebenezer
3. Babalola Ridwan

**ESTAM University**
