"use client";

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import styles from './Wheel.module.css';

// Dynamically import the wheel with SSR disabled
const RouletteWheel = dynamic(
    () => import('react-custom-roulette').then((mod) => mod.Wheel),
    { ssr: false }
);

interface WheelProps {
    items: string[];
    winningIndex?: number;
    onSpinComplete: (result: string) => void;
}

const Wheel: React.FC<WheelProps> = ({ items, winningIndex, onSpinComplete }) => {
    const [mustSpin, setMustSpin] = useState(false);
    const [prizeNumber, setPrizeNumber] = useState(0);

    if (!items || items.length === 0) return null;

    // Truncate text to max 12 characters for wheel display
    const truncateText = (text: string, maxLength: number = 12): string => {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    };

    // Convert items to the format expected by react-custom-roulette
    const data = items.map((item) => ({
        option: truncateText(item),
        style: {
            backgroundColor: '#8B0000',
            textColor: '#FFFFFF'
        }
    }));

    const handleSpinClick = () => {
        if (mustSpin) return;

        const newPrizeNumber = winningIndex !== undefined
            ? winningIndex
            : Math.floor(Math.random() * items.length);

        setPrizeNumber(newPrizeNumber);
        setMustSpin(true);
    };

    const handleStopSpinning = () => {
        setMustSpin(false);
        onSpinComplete(items[prizeNumber]);
    };

    return (
        <div className={styles.wheelContainer}>
            <RouletteWheel
                mustStartSpinning={mustSpin}
                prizeNumber={prizeNumber}
                data={data}
                onStopSpinning={handleStopSpinning}
                backgroundColors={['#1a0000', '#2a0000']}
                textColors={['#FFFFFF']}
                outerBorderColor="#C7B377"
                outerBorderWidth={8}
                innerBorderColor="#C7B377"
                innerBorderWidth={2}
                radiusLineColor="#C7B377"
                radiusLineWidth={2}
                fontSize={15}
                textDistance={60}
                spinDuration={0.4}
                pointerProps={{
                    src: '/dagger.png',
                    style: {
                        width: '60px',
                        height: '120px',
                        transform: 'rotate(245deg)',
                        top: -30,
                        right: 35,
                        animation: mustSpin ? 'daggerFlicker 0.08s ease-in-out infinite' : 'none'
                    }
                }}
            />
            <button className={styles.spinButton} onClick={handleSpinClick} disabled={mustSpin}>
                {mustSpin ? "FATE IS SEALED..." : "TEMPT FATE"}
            </button>
        </div>
    );
};

export default Wheel;
