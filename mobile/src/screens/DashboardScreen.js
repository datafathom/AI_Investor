
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';

export default function DashboardScreen() {
    const [refreshing, setRefreshing] = useState(false);
    const [data, setData] = useState({
        fearIndex: 50,
        portfolioValue: 100000,
        dailyChange: 1.25,
        status: 'ACTIVE'
    });

    const onRefresh = React.useCallback(() => {
        setRefreshing(true);
        // Simulate API fetch
        setTimeout(() => {
            setData(prev => ({
                ...prev,
                fearIndex: Math.floor(Math.random() * 100),
                dailyChange: (Math.random() * 4) - 2
            }));
            setRefreshing(false);
        }, 1000);
    }, []);

    return (
        <ScrollView
            style={styles.container}
            refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#fff" />}
        >
            {/* HEADER STATS */}
            <View style={styles.card}>
                <Text style={styles.label}>TOTAL EQUITY</Text>
                <Text style={styles.value}>${data.portfolioValue.toLocaleString()}</Text>
                <Text style={{ ...styles.subValue, color: data.dailyChange >= 0 ? '#4ade80' : '#f87171' }}>
                    {data.dailyChange > 0 ? '+' : ''}{data.dailyChange.toFixed(2)}% Today
                </Text>
            </View>

            {/* FEAR INDEX */}
            <View style={styles.card}>
                <Text style={styles.label}>FEAR & GREED INDEX</Text>
                <View style={styles.row}>
                    <Text style={styles.value}>{data.fearIndex}</Text>
                    <View style={{ ...styles.badge, backgroundColor: data.fearIndex > 50 ? '#22c55e' : '#ef4444' }}>
                        <Text style={styles.badgeText}>{data.fearIndex > 50 ? 'GREED' : 'FEAR'}</Text>
                    </View>
                </View>
                <View style={styles.progressBarBg}>
                    <View style={{ ...styles.progressBarFill, width: `${data.fearIndex}%`, backgroundColor: data.fearIndex > 50 ? '#22c55e' : '#ef4444' }} />
                </View>
            </View>

            {/* SYSTEM STATUS */}
            <View style={styles.card}>
                <Text style={styles.label}>SYSTEM STATUS</Text>
                <View style={styles.row}>
                    <Text style={styles.value}>{data.status}</Text>
                    <View style={styles.indicator} />
                </View>
            </View>

        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0f172a',
        padding: 16,
    },
    card: {
        backgroundColor: '#1e293b',
        borderRadius: 12,
        padding: 20,
        marginBottom: 16,
        borderWidth: 1,
        borderColor: '#334155'
    },
    label: {
        color: '#94a3b8',
        fontSize: 12,
        marginBottom: 8,
        fontWeight: 'bold',
        letterSpacing: 1,
    },
    value: {
        color: '#fff',
        fontSize: 32,
        fontWeight: 'bold',
    },
    subValue: {
        fontSize: 16,
        marginTop: 4,
    },
    row: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between'
    },
    badge: {
        paddingHorizontal: 12,
        paddingVertical: 4,
        borderRadius: 100,
    },
    badgeText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 12
    },
    progressBarBg: {
        height: 8,
        backgroundColor: '#334155',
        borderRadius: 4,
        marginTop: 16,
        overflow: 'hidden'
    },
    progressBarFill: {
        height: '100%',
        borderRadius: 4
    },
    indicator: {
        width: 12,
        height: 12,
        borderRadius: 6,
        backgroundColor: '#22c55e',
        shadowColor: '#22c55e',
        shadowOpacity: 0.8,
        shadowRadius: 10,
        elevation: 5
    }
});
