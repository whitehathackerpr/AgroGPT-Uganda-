import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import DiseaseScreen from './src/screens/DiseaseScreen';
import WeatherScreen from './src/screens/WeatherScreen';
import MarketScreen from './src/screens/MarketScreen';
import ProfileScreen from './src/screens/ProfileScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="Home"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#16a34a',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen 
            name="Home" 
            component={HomeScreen}
            options={{ title: 'AgroGPT Uganda' }}
          />
          <Stack.Screen 
            name="Disease" 
            component={DiseaseScreen}
            options={{ title: 'Disease Diagnosis' }}
          />
          <Stack.Screen 
            name="Weather" 
            component={WeatherScreen}
            options={{ title: 'Weather Forecast' }}
          />
          <Stack.Screen 
            name="Market" 
            component={MarketScreen}
            options={{ title: 'Market Prices' }}
          />
          <Stack.Screen 
            name="Profile" 
            component={ProfileScreen}
            options={{ title: 'My Profile' }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
} 