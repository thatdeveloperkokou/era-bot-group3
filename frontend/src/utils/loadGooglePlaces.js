// Utility to load Google Places API dynamically
export const loadGooglePlacesAPI = (apiKey) => {
  return new Promise((resolve, reject) => {
    // Check if already loaded
    if (window.google && window.google.maps && window.google.maps.places) {
      resolve(window.google);
      return;
    }

    // Check if script is already being loaded
    if (document.querySelector('script[data-google-places]')) {
      const checkInterval = setInterval(() => {
        if (window.google && window.google.maps && window.google.maps.places) {
          clearInterval(checkInterval);
          resolve(window.google);
        }
      }, 100);
      
      // Timeout after 10 seconds
      setTimeout(() => {
        clearInterval(checkInterval);
        reject(new Error('Google Places API loading timeout'));
      }, 10000);
      return;
    }

    // Create script element
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
    script.async = true;
    script.defer = true;
    script.setAttribute('data-google-places', 'true');
    
    script.onload = () => {
      if (window.google && window.google.maps && window.google.maps.places) {
        resolve(window.google);
      } else {
        reject(new Error('Google Places API failed to load'));
      }
    };
    
    script.onerror = () => {
      reject(new Error('Failed to load Google Places API script'));
    };
    
    document.head.appendChild(script);
  });
};

