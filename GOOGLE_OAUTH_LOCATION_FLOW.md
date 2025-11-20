# Google OAuth with Location Input

## ✅ What's Been Updated

I've updated the Google OAuth flow to require location input for new users, just like the email registration flow!

## 🎯 New Flow

### For New Users:
1. User clicks "Sign in with Google"
2. Google popup appears
3. User selects Google account
4. **Location input form appears** (NEW!)
5. User enters location using Mapbox autocomplete
6. Account created with location
7. User logged in and redirected to dashboard

### For Existing Users:
1. User clicks "Sign in with Google"
2. Google popup appears
3. User selects Google account
4. **Immediately logged in** (no location needed)
5. Redirected to dashboard

---

## 🔧 How It Works

### Backend Changes:

1. **`/api/auth/google`** (Updated):
   - Verifies Google token
   - If existing user → logs in immediately
   - If new user → returns user info (but doesn't create account yet)
   - Returns `isNewUser: true` with user data

2. **`/api/auth/google/complete`** (New):
   - Verifies Google token again
   - Receives location from frontend
   - Resolves region from location
   - Creates user account with location
   - Returns JWT token

### Frontend Changes:

1. **Google Sign-In Handler**:
   - If existing user → login immediately
   - If new user → show location form

2. **Location Form**:
   - Uses same `LocationAutocomplete` component
   - Same Mapbox integration
   - User enters location
   - Submits to `/api/auth/google/complete`

3. **UI Flow**:
   - Google button hidden when location form is shown
   - Location form matches verification form style
   - Cancel button to go back

---

## 🎨 User Experience

### New User Flow:
```
1. Click "Sign in with Google"
   ↓
2. Select Google account
   ↓
3. See: "Complete Your Registration"
   "Welcome, [Name]! Please provide your location to continue."
   ↓
4. Enter location (Mapbox autocomplete)
   ↓
5. Click "Complete Registration"
   ↓
6. Logged in → Dashboard
```

### Existing User Flow:
```
1. Click "Sign in with Google"
   ↓
2. Select Google account
   ↓
3. Immediately logged in → Dashboard
```

---

## ✅ Benefits

- ✅ **Consistent experience** - Same location input as email registration
- ✅ **Region mapping** - Location automatically maps to region for auto-logging
- ✅ **Complete data** - All users have location data
- ✅ **Better UX** - Clear flow, no confusion

---

## 📋 What's Required

### Location Input:
- Uses Mapbox autocomplete (same as email registration)
- Required field
- Region automatically inferred from location
- Same validation and error handling

### Backend:
- Two-step process for new users
- Token verification on both steps (security)
- Region resolution from location
- Account creation with complete data

---

## 🎉 Result

Now **all users** (email or Google) provide location during registration, ensuring:
- ✅ Complete user profiles
- ✅ Region mapping for auto-logging
- ✅ Consistent data collection
- ✅ Better user experience

---

**The Google OAuth flow now matches the email registration flow - users always provide location!** 🚀

