# Automatic Power Logging Flow

## Overview

Yes! The system automatically logs power ON/OFF events based on the user's registered location and their region's schedule template. Here's how it works:

## Complete Flow

### 1. User Registration with Location (Mapbox)

**Frontend:**
- User selects location using Mapbox geocoding (via `LocationAutocomplete` component)
- Location is saved as a text string (e.g., "Victoria Island, Lagos, Nigeria")

**Backend (`/api/register`):**
```python
location = data.get('location', '')
region_id = resolve_region_id(location)  # Infers region from location keywords

user = User(
    username=username,
    location=location,
    region_id=region_id,  # Automatically assigned based on location
    ...
)
```

**Region Inference:**
- Uses `region_mapper.py` to match location keywords to region profiles
- Example: "Victoria Island, Lagos" → matches "ikeja" region (EKEDC)
- Example: "Gwarinpa, Abuja" → matches "abuja" region (AEDC)

### 2. Automatic Power Logging (Hourly)

**Scheduler (`scheduler_runner.py`):**
- Runs continuously, executing `auto_logger.py` every hour
- Can be configured in Railway with start command: `python backend/scheduler_runner.py`

**Auto Logger (`auto_logger.py`):**
For each region:
1. Checks the region's `schedule_template` (derived from NERC Q2 2025 data)
2. Determines if power should be ON or OFF at the current time
3. For each user in that region:
   - Checks their last power log entry
   - If last log doesn't match expected state, creates a new log entry

**Example:**
```python
# If it's 2:00 PM and Ikeja region should have power ON
# (based on schedule_template blocks)
# And user's last log was "off" at 1:00 PM
# → Creates new log: event_type="on", auto_generated=True, timestamp=2:00 PM
```

### 3. Dashboard Display

**Stats Endpoint (`/api/stats`):**
- Fetches ALL power logs for the user (both manual and auto-generated)
- No filtering - includes logs with `auto_generated=True`
- Calculates total hours, daily stats, and chart data

**Dashboard Component:**
- Displays total light hours
- Shows daily statistics chart
- Includes both:
  - **Manual logs**: User clicks "Power ON/OFF" buttons
  - **Auto-generated logs**: Created by scheduler based on region schedule

## Key Features

✅ **Automatic Region Assignment**
- User's region is automatically inferred from their location during registration
- No manual selection needed

✅ **Hourly Auto-Logging**
- Scheduler runs every hour
- Creates power logs based on region's schedule template
- Only creates logs when state changes (doesn't duplicate)

✅ **Unified Dashboard Display**
- All logs (manual + auto) appear in dashboard
- Statistics include both types
- Charts show combined data

✅ **Region-Based Scheduling**
- Each of the 11 Nigerian DisCos has a schedule template
- Derived from NERC Q2 2025 report data
- Accounts for different power availability patterns per region

## Example User Journey

1. **User registers:**
   - Enters location: "Lekki, Lagos, Nigeria"
   - System infers: `region_id = "ikeja"` (EKEDC)

2. **First hour after registration:**
   - Scheduler runs at 3:00 PM
   - Checks Ikeja schedule: Power should be ON at 3:00 PM
   - User has no previous logs
   - Creates: `PowerLog(event_type="on", auto_generated=True, timestamp=3:00 PM)`

3. **User views dashboard:**
   - Sees "Total Light Hours: 1.0 hours" (if still on)
   - Chart shows power ON event at 3:00 PM

4. **Next hour (4:00 PM):**
   - Scheduler runs again
   - Checks schedule: Power should still be ON
   - Last log is already "on" → No new log created (no state change)

5. **Later (8:00 PM):**
   - Scheduler runs
   - Schedule indicates power should be OFF
   - Last log is "on" → Creates: `PowerLog(event_type="off", auto_generated=True, timestamp=8:00 PM)`

6. **User manually logs:**
   - User clicks "Power ON" button at 9:00 PM
   - Creates: `PowerLog(event_type="on", auto_generated=False, timestamp=9:00 PM)`
   - Dashboard shows both auto and manual logs

## Schedule Template Structure

Each region has a `schedule_template` with time blocks:
```json
[
  {"start": "06:00", "end": "10:00"},  // Power ON 6 AM - 10 AM
  {"start": "14:00", "end": "18:00"},  // Power ON 2 PM - 6 PM
  {"start": "20:00", "end": "22:00"}   // Power ON 8 PM - 10 PM
]
```

The auto logger checks if current time falls within any block to determine ON/OFF state.

## Important Notes

⚠️ **Initial Delay:**
- Auto-logging starts on the next hourly run after user registration
- If user registers at 2:30 PM, first auto-log will be at 3:00 PM (next hour)

⚠️ **State Change Only:**
- Auto logger only creates logs when state changes
- If power should be ON and last log is already ON → no new log
- This prevents duplicate entries

⚠️ **Manual Override:**
- Users can still manually log power events
- Manual logs take precedence (they're the actual state)
- Auto logger respects the last log (manual or auto) when determining if state change is needed

## Verification

To verify it's working:

1. **Check Database:**
   ```sql
   SELECT * FROM power_logs 
   WHERE user_id = 'your_username' 
   ORDER BY timestamp DESC;
   ```
   Look for entries with `auto_generated = true`

2. **Check Dashboard:**
   - View dashboard after waiting an hour
   - Should see new power events appearing automatically
   - Check timestamps - they should align with hourly schedule

3. **Check Scheduler Logs:**
   - Railway logs should show:
     ```
     Auto logger processed 11 regions and queued X events
     ```

## Configuration

**To enable auto-logging in Railway:**
1. Set service start command to: `python backend/scheduler_runner.py`
2. Or create separate Cron service pointing to backend
3. Ensure backend service has database access

**To test locally:**
```bash
# Run scheduler manually
python backend/scheduler_runner.py

# Or run auto logger once
python backend/auto_logger.py
```

