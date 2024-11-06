import React, { useState, useEffect } from 'react';
import axios from 'axios';

const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
};

const App: React.FC = () => {
    const [timeLeft, setTimeLeft] = useState<number>(0);
    const [isActive, setIsActive] = useState<boolean>(false);
    const [repeatsLeft, setRepeatsLeft] = useState<number>(0);

    useEffect(() => {
        const fetchCountdown = async () => {
            try {
                const response = await axios.get('http://localhost:8000/countdown');
                console.log(response)
                setTimeLeft(response.data.time_left);
                setIsActive(response.data.active);
                setRepeatsLeft(response.data.repeats);
            } catch (error) {
                console.error("Error fetching countdown status", error);
            }
        };

        fetchCountdown();
        const interval = setInterval(fetchCountdown, 1000); // Fetch every second

        return () => clearInterval(interval);
    }, []);

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Countdown Timer</h1>
            <h2>Status: {isActive ? "Active" : "Inactive"}</h2>
            {isActive && (
                <>
                    <h3>Time Left: {formatTime(timeLeft)}</h3>
                    <h3>Repeats Left: {repeatsLeft}</h3>
                </>
            )}
        </div>
    );
};

export default App;
