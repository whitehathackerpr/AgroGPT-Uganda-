import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Import screens
import HomeScreen from './src/screens/HomeScreen';
import DiseaseScreen from './src/screens/DiseaseScreen';
import WeatherScreen from './src/screens/WeatherScreen';
import MarketScreen from './src/screens/MarketScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Stack = createNativeStackNavigator();

const App = () => {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="Home"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#22c55e', // green-600
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
            name="Settings" 
            component={SettingsScreen}
            options={{ title: 'Settings' }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
};

export default App; 