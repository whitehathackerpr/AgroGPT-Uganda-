import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  useWindowDimensions,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Disease: undefined;
  Weather: undefined;
  Market: undefined;
  Settings: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

const HomeScreen = () => {
  const navigation = useNavigation<NavigationProp>();
  const { width } = useWindowDimensions();

  const menuItems = [
    {
      title: 'Disease Diagnosis',
      icon: 'microscope',
      screen: 'Disease',
      color: '#ef4444', // red-500
    },
    {
      title: 'Weather Forecast',
      icon: 'weather-partly-cloudy',
      screen: 'Weather',
      color: '#3b82f6', // blue-500
    },
    {
      title: 'Market Prices',
      icon: 'chart-line',
      screen: 'Market',
      color: '#f59e0b', // amber-500
    },
    {
      title: 'Settings',
      icon: 'cog',
      screen: 'Settings',
      color: '#6b7280', // gray-500
    },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Welcome to AgroGPT</Text>
        <Text style={styles.subtitle}>Your Smart Farming Assistant</Text>
      </View>
      
      <View style={styles.grid}>
        {menuItems.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={[
              styles.card,
              { width: width / 2 - 24 }, // Accounting for margins
              { backgroundColor: item.color }
            ]}
            onPress={() => navigation.navigate(item.screen)}
          >
            <Icon name={item.icon} size={40} color="#fff" />
            <Text style={styles.cardText}>{item.title}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f3f4f6', // gray-100
  },
  header: {
    padding: 20,
    backgroundColor: '#22c55e', // green-600
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#fff',
    textAlign: 'center',
    marginTop: 8,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 8,
    justifyContent: 'center',
  },
  card: {
    height: 150,
    margin: 8,
    borderRadius: 12,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  cardText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 12,
    textAlign: 'center',
  },
});

export default HomeScreen; 