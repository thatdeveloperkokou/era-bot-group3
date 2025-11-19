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

  // Improved search for street-level addresses in Nigeria
  // Try multiple search strategies to get better street results
  const searchParams = new URLSearchParams({
    access_token: token,
    autocomplete: 'true',
    country: options.countryCode || DEFAULT_COUNTRY,
    limit: limit.toString(),
    language: 'en',
    // Focus on street-level types first; Mapbox only accepts specific type keywords
    types: options.types || 'address,poi,neighborhood,district,place,locality',
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
    let features = (data.features || []).map(normalizeFeature);
    
    // If we don't have enough address results, try a secondary search with broader types
    const addressResults = features.filter(f => 
      f.mapboxFeature?.place_type?.includes('address') || 
      f.mapboxFeature?.place_type?.includes('street')
    );
    
    // If query looks like a street name (contains common street indicators), do additional search
    const queryLower = query.trim().toLowerCase();
    const isStreetQuery = /street|st|road|rd|avenue|ave|drive|dr|close|cl|way|boulevard|blvd|lane|ln/i.test(queryLower) ||
                         queryLower.split(' ').length >= 2; // Multi-word queries are more likely streets
    
    if (addressResults.length < 3 && isStreetQuery) {
      // Try a more specific address search
      try {
        const addressParams = new URLSearchParams({
          access_token: token,
          autocomplete: 'true',
          country: options.countryCode || DEFAULT_COUNTRY,
          limit: '5',
          language: 'en',
          types: 'address,poi', // Restrict to valid Mapbox types
        });
        
        const addressResponse = await fetch(`${MAPBOX_BASE_URL}/${encodedQuery}.json?${addressParams.toString()}`);
        if (addressResponse.ok) {
          const addressData = await addressResponse.json();
          const addressFeatures = (addressData.features || []).map(normalizeFeature);
          // Merge and deduplicate
          const existingIds = new Set(features.map(f => f.place_id));
          addressFeatures.forEach(f => {
            if (!existingIds.has(f.place_id)) {
              features.push(f);
              existingIds.add(f.place_id);
            }
          });
        }
      } catch (e) {
        console.warn('Secondary address search failed:', e);
      }
    }
    
    // Sort results to prioritize street addresses and POIs over cities/towns
    const typePriority = {
      'address': 1,
      'street': 1,
      'poi': 2,
      'neighborhood': 3,
      'district': 4,
      'postcode': 5,
      'place': 6,
      'locality': 7,
      'region': 8
    };
    
    return features.sort((a, b) => {
      const aType = a.mapboxFeature?.place_type?.[0] || '';
      const bType = b.mapboxFeature?.place_type?.[0] || '';
      const aPriority = typePriority[aType] || 99;
      const bPriority = typePriority[bType] || 99;
      
      // If same priority, prefer results with "street" or "road" in the name
      if (aPriority === bPriority) {
        const aName = (a.description || '').toLowerCase();
        const bName = (b.description || '').toLowerCase();
        const aHasStreet = /street|road|avenue|drive|way|boulevard|lane/i.test(aName);
        const bHasStreet = /street|road|avenue|drive|way|boulevard|lane/i.test(bName);
        if (aHasStreet && !bHasStreet) return -1;
        if (!aHasStreet && bHasStreet) return 1;
      }
      
      return aPriority - bPriority;
    });
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

