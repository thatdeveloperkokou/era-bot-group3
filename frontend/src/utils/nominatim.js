// OpenStreetMap Nominatim Geocoding API utility
// Free, no API key required, no credit card needed
// Rate limit: 1 request per second (more than enough for registration)

const NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org';

/**
 * Search for locations using OpenStreetMap Nominatim
 * @param {string} query - Search query
 * @param {number} limit - Maximum number of results (default: 5)
 * @returns {Promise<Array>} Array of location results
 */
export const searchLocations = async (query, limit = 5) => {
  if (!query || query.trim().length < 2) {
    return [];
  }

  try {
    const params = new URLSearchParams({
      q: query,
      format: 'json',
      addressdetails: '1',
      limit: limit.toString(),
      countrycodes: '', // Empty for worldwide, or specify like 'ng' for Nigeria
    });

    const response = await fetch(`${NOMINATIM_BASE_URL}/search?${params}`, {
      headers: {
        'User-Agent': 'Electricity Logger App', // Required by Nominatim
        'Accept-Language': 'en',
      },
    });

    if (!response.ok) {
      throw new Error(`Nominatim API error: ${response.status}`);
    }

    const data = await response.json();
    
    // Transform Nominatim results to a format similar to Google Places
    return data.map((result) => ({
      place_id: result.place_id,
      description: result.display_name,
      formatted_address: result.display_name,
      address_components: result.address || {},
      geometry: {
        location: {
          lat: parseFloat(result.lat),
          lng: parseFloat(result.lon),
        },
      },
      types: result.type ? [result.type] : [],
      // Additional Nominatim-specific data
      osm_type: result.osm_type,
      osm_id: result.osm_id,
      boundingbox: result.boundingbox,
    }));
  } catch (error) {
    console.error('Error searching locations with Nominatim:', error);
    return [];
  }
};

/**
 * Reverse geocode - Get address from coordinates
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {Promise<Object|null>} Location data or null
 */
export const reverseGeocode = async (lat, lng) => {
  try {
    const params = new URLSearchParams({
      lat: lat.toString(),
      lon: lng.toString(),
      format: 'json',
      addressdetails: '1',
    });

    const response = await fetch(`${NOMINATIM_BASE_URL}/reverse?${params}`, {
      headers: {
        'User-Agent': 'Electricity Logger App',
        'Accept-Language': 'en',
      },
    });

    if (!response.ok) {
      throw new Error(`Nominatim API error: ${response.status}`);
    }

    const data = await response.json();
    
    return {
      place_id: data.place_id,
      description: data.display_name,
      formatted_address: data.display_name,
      address_components: data.address || {},
      geometry: {
        location: {
          lat: parseFloat(data.lat),
          lng: parseFloat(data.lon),
        },
      },
    };
  } catch (error) {
    console.error('Error reverse geocoding with Nominatim:', error);
    return null;
  }
};

/**
 * Get location details from a place ID
 * @param {string} placeId - Place ID from Nominatim
 * @returns {Promise<Object|null>} Location data or null
 */
export const getPlaceDetails = async (placeId) => {
  try {
    // Nominatim doesn't have a direct place_id lookup, so we use the OSM type and ID
    // This is a simplified version - in practice, you'd store the full result
    const params = new URLSearchParams({
      place_id: placeId,
      format: 'json',
      addressdetails: '1',
    });

    const response = await fetch(`${NOMINATIM_BASE_URL}/lookup?${params}`, {
      headers: {
        'User-Agent': 'Electricity Logger App',
        'Accept-Language': 'en',
      },
    });

    if (!response.ok) {
      throw new Error(`Nominatim API error: ${response.status}`);
    }

    const data = await response.json();
    
    if (data && data.length > 0) {
      const result = data[0];
      return {
        place_id: result.place_id,
        description: result.display_name,
        formatted_address: result.display_name,
        address_components: result.address || {},
        geometry: {
          location: {
            lat: parseFloat(result.lat),
            lng: parseFloat(result.lon),
          },
        },
      };
    }
    
    return null;
  } catch (error) {
    console.error('Error getting place details from Nominatim:', error);
    return null;
  }
};

// Debounce function to limit API calls
let searchTimeout = null;
export const debouncedSearch = (query, callback, delay = 500) => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  
  searchTimeout = setTimeout(async () => {
    const results = await searchLocations(query);
    callback(results);
  }, delay);
};

