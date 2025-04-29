import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import * as Location from 'expo-location';
import axios from 'axios';

interface WeatherData {
  temperature_c: number;
  humidity: number;
  wind_kph: number;
  rainfall_mm: number;
  uv_index: number;
}

const WeatherScreen = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [location, setLocation] = useState<string | null>(null);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [forecast, setForecast] = useState<any[]>([]);

  const getLocationAndWeather = async () => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        alert('Permission to access location was denied');
        return;
      }

      const location = await Location.getCurrentPositionAsync({});
      const { latitude, longitude } = location.coords;
      
      // Get location name
      const response = await Location.reverseGeocodeAsync({
        latitude,
        longitude
      });

      if (response[0]) {
        const locationName = `${response[0].city || response[0].district}, ${response[0].country}`;
        setLocation(locationName);
        await fetchWeatherData(locationName);
      }
    } catch (error) {
      console.error(error);
      alert('Error getting location');
    } finally {
      setLoading(false);
    }
  };

  const fetchWeatherData = async (locationName: string) => {
    try {
      const [currentResponse, forecastResponse] = await Promise.all([
        axios.get(`http://localhost:8000/api/weather/agricultural-metrics/${locationName}`),
        axios.get(`http://localhost:8000/api/weather/forecast/${locationName}`)
      ]);

      setWeatherData(currentResponse.data);
      setForecast(forecastResponse.data);
    } catch (error) {
      console.error(error);
      alert('Error fetching weather data');
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    if (location) {
      await fetchWeatherData(location);
    }
    setRefreshing(false);
  };

  useEffect(() => {
    getLocationAndWeather();
  }, []);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#16a34a" />
        <Text style={styles.loadingText}>Loading weather data...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Location Header */}
      <View style={styles.header}>
        <Text style={styles.location}>{location}</Text>
      </View>

      {/* Current Weather */}
      {weatherData && (
        <View style={styles.currentWeather}>
          <Text style={styles.sectionTitle}>Current Conditions</Text>
          <View style={styles.weatherGrid}>
            <View style={styles.weatherItem}>
              <Text style={styles.weatherValue}>{weatherData.temperature_c}°C</Text>
              <Text style={styles.weatherLabel}>Temperature</Text>
            </View>
            <View style={styles.weatherItem}>
              <Text style={styles.weatherValue}>{weatherData.humidity}%</Text>
              <Text style={styles.weatherLabel}>Humidity</Text>
            </View>
            <View style={styles.weatherItem}>
              <Text style={styles.weatherValue}>{weatherData.wind_kph} km/h</Text>
              <Text style={styles.weatherLabel}>Wind Speed</Text>
            </View>
            <View style={styles.weatherItem}>
              <Text style={styles.weatherValue}>{weatherData.rainfall_mm} mm</Text>
              <Text style={styles.weatherLabel}>Rainfall</Text>
            </View>
          </View>
        </View>
      )}

      {/* Forecast */}
      {forecast.length > 0 && (
        <View style={styles.forecast}>
          <Text style={styles.sectionTitle}>7-Day Forecast</Text>
          {forecast.map((day, index) => (
            <View key={index} style={styles.forecastDay}>
              <Text style={styles.dayText}>{day.date}</Text>
              <View style={styles.forecastDetails}>
                <Text style={styles.forecastTemp}>
                  {day.day.avgtemp_c}°C
                </Text>
                <Text style={styles.forecastDesc}>
                  {day.day.condition.text}
                </Text>
              </View>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#6b7280',
  },
  header: {
    padding: 20,
    backgroundColor: '#16a34a',
    alignItems: 'center',
  },
  location: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  currentWeather: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 16,
  },
  weatherGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  weatherItem: {
    width: '48%',
    backgroundColor: '#ffffff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  weatherValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#16a34a',
    marginBottom: 4,
  },
  weatherLabel: {
    fontSize: 14,
    color: '#6b7280',
  },
  forecast: {
    padding: 20,
  },
  forecastDay: {
    backgroundColor: '#ffffff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  dayText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  forecastDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  forecastTemp: {
    fontSize: 18,
    color: '#16a34a',
    fontWeight: 'bold',
  },
  forecastDesc: {
    fontSize: 14,
    color: '#6b7280',
  },
});

export default WeatherScreen; 