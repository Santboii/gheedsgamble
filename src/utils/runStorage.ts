import { Challenge } from '@/data';

export interface Run {
    id: string;
    timestamp: number;
    className: string;
    build: string;
    challenges: Challenge[];
    status: 'active' | 'completed' | 'failed';
    notes?: string;
}

const STORAGE_KEY = 'gheed_gamble_runs';

// Get all runs from localStorage
export const getRuns = (): Run[] => {
    if (typeof window === 'undefined') return [];
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    } catch (error) {
        console.error('Error reading runs from localStorage:', error);
        return [];
    }
};

// Save a new run
export const saveRun = (run: Omit<Run, 'id' | 'timestamp'>): Run => {
    const newRun: Run = {
        ...run,
        id: `run_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: Date.now()
    };

    const runs = getRuns();
    runs.unshift(newRun); // Add to beginning
    localStorage.setItem(STORAGE_KEY, JSON.stringify(runs));
    return newRun;
};

// Update run status
export const updateRunStatus = (id: string, status: Run['status'], notes?: string): void => {
    const runs = getRuns();
    const runIndex = runs.findIndex(r => r.id === id);
    if (runIndex !== -1) {
        runs[runIndex].status = status;
        if (notes !== undefined) {
            runs[runIndex].notes = notes;
        }
        localStorage.setItem(STORAGE_KEY, JSON.stringify(runs));
    }
};

// Delete a run
export const deleteRun = (id: string): void => {
    const runs = getRuns();
    const filtered = runs.filter(r => r.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
};

// Export runs as JSON
export const exportRuns = (): void => {
    const runs = getRuns();
    const dataStr = JSON.stringify(runs, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `gheed_gamble_runs_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
};

// Import runs from JSON
export const importRuns = (file: File): Promise<void> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const imported = JSON.parse(e.target?.result as string) as Run[];
                const existing = getRuns();
                // Merge, avoiding duplicates by ID
                const merged = [...imported];
                existing.forEach(run => {
                    if (!merged.find(r => r.id === run.id)) {
                        merged.push(run);
                    }
                });
                localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
                resolve();
            } catch (error) {
                reject(error);
            }
        };
        reader.onerror = reject;
        reader.readAsText(file);
    });
};
