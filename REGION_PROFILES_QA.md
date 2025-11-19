# Region Profiles QA - Frontend Integration

## Summary

Added region profiles display to the Dashboard component to verify the `/api/region-profiles` endpoint and display region data.

## Changes Made

### 1. Frontend Dashboard (`frontend/src/components/Dashboard.js`)
- Added region profiles section with collapsible display
- Fetches data from `/api/region-profiles` endpoint
- Displays:
  - Total number of regions
  - Region details including:
    - DisCo name
    - Region ID
    - States covered
    - Average offtake (MWh/h)
    - Average available PCC (MWh/h)
    - Utilization percentage
    - Estimated daily MWh
    - Full load hours
    - Schedule blocks count

### 2. Backend API (`backend/app.py`)
- Added OPTIONS method handling for CORS support
- Endpoint: `GET /api/region-profiles`
- Returns: `{ "regions": [...] }` with all region profile data

## Testing the Endpoint

### Option 1: Via Frontend Dashboard
1. Log in to the application
2. Navigate to the Dashboard
3. Scroll down to the "Region Profiles" section
4. Click "Show Regions" button
5. Verify the data loads and displays correctly

### Option 2: Direct API Call
```bash
# Using curl
curl https://era-bot-group3-production.up.railway.app/api/region-profiles

# Using PowerShell
Invoke-WebRequest -Uri "https://era-bot-group3-production.up.railway.app/api/region-profiles" -Method GET

# Using Node.js test script
node test_region_profiles_api.js
```

### Expected Response Format
```json
{
  "regions": [
    {
      "id": "abuja",
      "disco_name": "Abuja Electricity Distribution Plc (AEDC)",
      "states": ["fct", "abuja", "niger", "kogi", "nasarawa"],
      "keywords": ["abuja", "fct", "gwarinpa", "lokoja", "mina", "lafia"],
      "avg_offtake_mwh_per_hour": 547.84,
      "avg_available_pcc_mwh_per_hour": 611.00,
      "utilisation_percent": 89.66,
      "estimated_daily_mwh": 13148.16,
      "estimated_full_load_hours": 21.5,
      "schedule_template": [...],
      "source": "NERC Q2 2025",
      "updated_at": "2025-01-XX..."
    },
    ...
  ]
}
```

## Verification Checklist

- [ ] Backend service is deployed and running
- [ ] `/api/region-profiles` endpoint returns 200 status
- [ ] Response contains `regions` array
- [ ] Region count matches expected number (should be 11 DisCos)
- [ ] Each region has required fields populated
- [ ] Frontend dashboard displays region profiles correctly
- [ ] Region data numbers match NERC Q2 2025 report

## Expected Region Count

Based on NERC Q2 2025 data, there should be **11 Distribution Companies (DisCos)**:
1. Abuja (AEDC)
2. Benin (BEDC)
3. Eko (EKEDC)
4. Enugu (EEDC)
5. Ibadan (IBEDC)
6. Ikeja (IE)
7. Jos (JEDC)
8. Kaduna (KAEDCO)
9. Kano (KEDCO)
10. Port Harcourt (PHEDC)
11. Yola (YEDC)

## Troubleshooting

### 404 Error
- Verify backend service is deployed
- Check Railway logs for deployment errors
- Ensure the route is registered correctly

### CORS Errors
- Verify OPTIONS method is handled
- Check CORS configuration in `app.py`
- Ensure frontend API URL is correct

### Empty Response
- Check database connection
- Verify region profiles are seeded in database
- Run `python backend/region_profiles_seed.py` if needed

### Frontend Not Loading
- Check browser console for errors
- Verify API URL in `frontend/src/services/api.js`
- Check network tab for failed requests

## Next Steps

1. Deploy backend changes to Railway
2. Test endpoint directly via API call
3. Test via frontend dashboard
4. Verify all 11 regions are present
5. Confirm numbers match NERC Q2 2025 data

