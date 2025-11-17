// Mapbox Geocoding API utility.
// Requires a Mapbox access token (set REACT_APP_MAPBOX_ACCESS_TOKEN).

const MAPBOX_BASE_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places';
const DEFAULT_COUNTRY = 'NG'; // Limit searches to Nigeria.

const mapboxToken = () => {
  const token = process.env.REACT_APP_MAPBOX_ACCESS_TOKEN;
  if (!token) {
    console.warn('Missing REACT_APP_MAPBOX_ACCESS_TOKEN. Mapbox searches will be skipped.');
  }
  return token;
};

const normalizeFeature = (feature) => ({
  place_id: feature.id,
  description: feature.place_name,
  formatted_address: feature.place_name,
  address_components: feature.context || [],
  geometry: {
    location: {
      lat: feature.center?.[1],
      lng: feature.center?.[0],
    },
  },
  mapboxFeature: feature,
});

/**
 * Search for locations using Mapbox (Nigeria-only by default).
 * @param {string} query - Search query
 * @param {number} limit - Max number of results
 * @param {object} options - Optional overrides (countryCode, proximity, types)
 */
export const searchLocations = async (query, limit = 5, options = {}) => {
  const token = mapboxToken();
  if (!token || !query || query.trim().length < 2) {
    return [];
  }

  const searchParams = new URLSearchParams({
    access_token: token,
    autocomplete: 'true',
    country: options.countryCode || DEFAULT_COUNTRY,
    limit: limit.toString(),
    language: 'en',
    types: options.types || 'address,place,locality,region,neighborhood',
  });

  if (options.proximity?.lng && options.proximity?.lat) {
    searchParams.set('proximity', `${options.proximity.lng},${options.proximity.lat}`);
  }

  try {
    const encodedQuery = encodeURIComponent(query.trim());
    const response = await fetch(`${MAPBOX_BASE_URL}/${encodedQuery}.json?${searchParams.toString()}`);

    if (!response.ok) {
      throw new Error(`Mapbox API error: ${response.status}`);
    }

    const data = await response.json();
    return (data.features || []).map(normalizeFeature);
  } catch (error) {
    console.error('Error searching locations with Mapbox:', error);
    return [];
  }
};

/**
 * Reverse geocode coordinates using Mapbox (Nigeria-only by default).
 * @param {number} lat
 * @param {number} lng
 */
export const reverseGeocode = async (lat, lng) => {
  const token = mapboxToken();
  if (!token || typeof lat !== 'number' || typeof lng !== 'number') {
    return null;
  }

  const params = new URLSearchParams({
    access_token: token,
    country: DEFAULT_COUNTRY,
    language: 'en',
    limit: '1',
  });

  try {
    const response = await fetch(`${MAPBOX_BASE_URL}/${lng},${lat}.json?${params.toString()}`);
    if (!response.ok) {
      throw new Error(`Mapbox reverse geocode error: ${response.status}`);
    }

    const data = await response.json();
    const feature = data.features?.[0];
    return feature ? normalizeFeature(feature) : null;
  } catch (error) {
    console.error('Error reverse geocoding with Mapbox:', error);
    return null;
  }
};

/**
 * Fetch a single place by mapbox id (uses forward geocoding lookup).
 * @param {string} placeId
 */
export const getPlaceDetails = async (placeId) => {
  if (!placeId) {
    return null;
  }

  // Mapbox IDs are resolvable via forward geocoding with mapbox.places endpoint.
  const results = await searchLocations(placeId, 1, { types: '' });
  return results[0] || null;
};

