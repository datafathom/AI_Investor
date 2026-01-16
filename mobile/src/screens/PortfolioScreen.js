
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function PortfolioScreen() {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Portfolio Positions Placeholder</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0f172a',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        color: '#94a3b8'
    }
});
