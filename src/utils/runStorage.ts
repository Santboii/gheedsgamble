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

// Get all runs from API
export const getRuns = async (): Promise<Run[]> => {
    try {
        const response = await fetch('/api/runs');
        if (!response.ok) {
            if (response.status === 401) {
                // User not authenticated, return empty array
                return [];
            }
            throw new Error('Failed to fetch runs');
        }
        return await response.json();
    } catch (error) {
        console.error('Error reading runs from API:', error);
        return [];
    }
};

// Save a new run
export const saveRun = async (run: Omit<Run, 'id' | 'timestamp'>): Promise<Run | null> => {
    try {
        const response = await fetch('/api/runs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(run),
        });

        if (!response.ok) {
            throw new Error('Failed to save run');
        }

        return await response.json();
    } catch (error) {
        console.error('Error saving run:', error);
        return null;
    }
};

// Update run status
export const updateRunStatus = async (id: string, status: Run['status'], notes?: string): Promise<boolean> => {
    try {
        const response = await fetch(`/api/runs/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status, notes }),
        });

        return response.ok;
    } catch (error) {
        console.error('Error updating run status:', error);
        return false;
    }
};

// Delete a run
export const deleteRun = async (id: string): Promise<boolean> => {
    try {
        const response = await fetch(`/api/runs/${id}`, {
            method: 'DELETE',
        });

        return response.ok;
    } catch (error) {
        console.error('Error deleting run:', error);
        return false;
    }
};

// Export runs as JSON
export const exportRuns = (runs: Run[]): void => {
    const dataStr = JSON.stringify(runs, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `gheed_gamble_runs_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
};

// Import runs from JSON (for migration or backup restore)
export const importRuns = async (file: File): Promise<Run[]> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const imported = JSON.parse(e.target?.result as string) as Run[];

                // Import each run via API
                const importedRuns: Run[] = [];
                for (const run of imported) {
                    const { id, timestamp, ...runData } = run;
                    const newRun = await saveRun(runData);
                    if (newRun) {
                        importedRuns.push(newRun);
                    }
                }

                resolve(importedRuns);
            } catch (error) {
                reject(error);
            }
        };
        reader.onerror = reject;
        reader.readAsText(file);
    });
};
