
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'expo-status-bar';

// Screens
import DashboardScreen from './src/screens/DashboardScreen';
import PortfolioScreen from './src/screens/PortfolioScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();

export default function App() {
    return (
        <NavigationContainer>
            <StatusBar style="light" />
            <Tab.Navigator
                screenOptions={{
                    tabBarStyle: { backgroundColor: '#0f172a', borderTopColor: '#1e293b' },
                    tabBarActiveTintColor: '#22d3ee', // Cyan-400
                    tabBarInactiveTintColor: '#64748b', // Slate-500
                    headerStyle: { backgroundColor: '#0f172a' },
                    headerTintColor: '#fff',
                }}
            >
                <Tab.Screen name="Mission Control" component={DashboardScreen} />
                <Tab.Screen name="Portfolio" component={PortfolioScreen} />
                <Tab.Screen name="Settings" component={SettingsScreen} />
            </Tab.Navigator>
        </NavigationContainer>
    );
}
