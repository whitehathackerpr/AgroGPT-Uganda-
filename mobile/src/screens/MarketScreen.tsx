import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  RefreshControl,
  TouchableOpacity,
} from 'react-native';
import axios from 'axios';

interface MarketPrice {
  crop: string;
  price: number;
  unit: string;
  location: string;
  date: string;
}

const MarketScreen = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [marketPrices, setMarketPrices] = useState<MarketPrice[]>([]);
  const [selectedCrop, setSelectedCrop] = useState<string | null>(null);

  const fetchMarketPrices = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/market/prices');
      setMarketPrices(response.data);
    } catch (error) {
      console.error(error);
      alert('Error fetching market prices');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchMarketPrices();
    setRefreshing(false);
  };

  useEffect(() => {
    fetchMarketPrices();
  }, []);

  const uniqueCrops = [...new Set(marketPrices.map(price => price.crop))];

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#16a34a" />
        <Text style={styles.loadingText}>Loading market prices...</Text>
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
      {/* Crop Filter */}
      <View style={styles.filterContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <TouchableOpacity
            style={[
              styles.filterButton,
              !selectedCrop && styles.filterButtonActive
            ]}
            onPress={() => setSelectedCrop(null)}
          >
            <Text style={[
              styles.filterButtonText,
              !selectedCrop && styles.filterButtonTextActive
            ]}>All</Text>
          </TouchableOpacity>
          {uniqueCrops.map((crop) => (
            <TouchableOpacity
              key={crop}
              style={[
                styles.filterButton,
                selectedCrop === crop && styles.filterButtonActive
              ]}
              onPress={() => setSelectedCrop(crop)}
            >
              <Text style={[
                styles.filterButtonText,
                selectedCrop === crop && styles.filterButtonTextActive
              ]}>{crop}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Market Prices List */}
      <View style={styles.pricesContainer}>
        {marketPrices
          .filter(price => !selectedCrop || price.crop === selectedCrop)
          .map((price, index) => (
            <View key={index} style={styles.priceCard}>
              <View style={styles.priceHeader}>
                <Text style={styles.cropName}>{price.crop}</Text>
                <Text style={styles.price}>
                  UGX {price.price.toLocaleString()} / {price.unit}
                </Text>
              </View>
              <View style={styles.priceDetails}>
                <Text style={styles.location}>{price.location}</Text>
                <Text style={styles.date}>{new Date(price.date).toLocaleDateString()}</Text>
              </View>
            </View>
          ))}
      </View>
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
  filterContainer: {
    padding: 16,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  filterButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    backgroundColor: '#f3f4f6',
  },
  filterButtonActive: {
    backgroundColor: '#16a34a',
  },
  filterButtonText: {
    fontSize: 14,
    color: '#4b5563',
  },
  filterButtonTextActive: {
    color: '#ffffff',
    fontWeight: 'bold',
  },
  pricesContainer: {
    padding: 16,
  },
  priceCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
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
  priceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  cropName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  price: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#16a34a',
  },
  priceDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  location: {
    fontSize: 14,
    color: '#6b7280',
  },
  date: {
    fontSize: 14,
    color: '#6b7280',
  },
});

export default MarketScreen; 