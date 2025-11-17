import React, { useState, useEffect, useRef } from 'react';
import { searchLocations } from '../utils/mapboxGeocoding';
import './LocationAutocomplete.css';

const LocationAutocomplete = ({ value, onChange, onSelect, placeholder = 'Enter your location', required = false }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [searchQuery, setSearchQuery] = useState(value || '');
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);
  const searchTimeoutRef = useRef(null);

  useEffect(() => {
    setSearchQuery(value || '');
  }, [value]);

  useEffect(() => {
    // Clear previous timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    // Don't search if query is too short
    if (!searchQuery || searchQuery.trim().length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    // Debounce search to avoid too many API calls
    setLoading(true);
    searchTimeoutRef.current = setTimeout(async () => {
      try {
        // Increase limit for better street address results, especially for Nigeria
        const results = await searchLocations(searchQuery, 8);
        setSuggestions(results);
        setShowSuggestions(results.length > 0);
        setActiveIndex(-1);
      } catch (error) {
        console.error('Error fetching locations:', error);
        setSuggestions([]);
        setShowSuggestions(false);
      } finally {
        setLoading(false);
      }
    }, 500); // 500ms debounce

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [searchQuery]);

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setSearchQuery(newValue);
    onChange(newValue);
    setShowSuggestions(true);
  };

  const handleSelect = (suggestion) => {
    const address = suggestion.formatted_address || suggestion.description;
    setSearchQuery(address);
    setSuggestions([]);
    setShowSuggestions(false);
    setActiveIndex(-1);
    onChange(address);
    
    if (onSelect) {
      onSelect({
        address,
        lat: suggestion.geometry?.location?.lat,
        lng: suggestion.geometry?.location?.lng,
        placeId: suggestion.place_id,
        fullData: suggestion,
      });
    }
  };

  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) {
      if (e.key === 'Enter') {
        e.preventDefault();
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex((prev) => 
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex((prev) => (prev > 0 ? prev - 1 : -1));
        break;
      case 'Enter':
        e.preventDefault();
        if (activeIndex >= 0 && activeIndex < suggestions.length) {
          handleSelect(suggestions[activeIndex]);
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        setActiveIndex(-1);
        break;
      default:
        break;
    }
  };

  const handleBlur = (e) => {
    // Delay hiding suggestions to allow click events to fire
    setTimeout(() => {
      setShowSuggestions(false);
      setActiveIndex(-1);
    }, 200);
  };

  const handleFocus = () => {
    if (suggestions.length > 0) {
      setShowSuggestions(true);
    }
  };

  return (
    <div className="location-autocomplete">
      <div className="location-autocomplete-input-wrapper">
        <input
          ref={inputRef}
          type="text"
          value={searchQuery}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onBlur={handleBlur}
          onFocus={handleFocus}
          placeholder={placeholder}
          className="location-input"
          autoComplete="off"
          required={required}
        />
        {loading && (
          <div className="location-autocomplete-spinner">
            <div className="spinner"></div>
          </div>
        )}
      </div>
      {showSuggestions && suggestions.length > 0 && (
        <div 
          ref={suggestionsRef}
          className="autocomplete-dropdown"
          role="listbox"
        >
          {suggestions.map((suggestion, index) => {
            const isActive = index === activeIndex;
            const address = suggestion.formatted_address || suggestion.description;
            
            return (
              <div
                key={suggestion.place_id || index}
                className={`suggestion-item ${isActive ? 'active' : ''}`}
                onClick={() => handleSelect(suggestion)}
                onMouseEnter={() => setActiveIndex(index)}
                role="option"
                aria-selected={isActive}
              >
                <span>{address}</span>
              </div>
            );
          })}
        </div>
      )}
      {showSuggestions && !loading && suggestions.length === 0 && searchQuery.length >= 2 && (
        <div className="autocomplete-dropdown">
          <div className="suggestion-item no-results">
            No locations found. Try a different search.
          </div>
        </div>
      )}
    </div>
  );
};

export default LocationAutocomplete;

