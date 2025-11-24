"use client";

import { useState, useEffect } from "react";
import Wheel from "@/components/Wheel";
import { CLASSES, BUILDS, CHALLENGES, ClassName, Challenge } from "@/data";
import { getRuns, saveRun, updateRunStatus, deleteRun, exportRuns, importRuns, Run } from "@/utils/runStorage";
import styles from "./page.module.css";

type Step = "CONFIG" | "CLASS" | "BUILD" | "CHALLENGE" | "RESULT";

interface Config {
  rerolls: number;
  challengeCount: number;
}

interface SelectionState {
  className: ClassName | null;
  build: string | null;
  challenges: Challenge[];
}

export default function Home() {
  const [step, setStep] = useState<Step>("CONFIG");
  const [config, setConfig] = useState<Config>({ rerolls: 1, challengeCount: 1 });
  const [selections, setSelections] = useState<SelectionState>({
    className: null,
    build: null,
    challenges: []
  });
  const [rerollsLeft, setRerollsLeft] = useState(0);

  // Temporary state for the current spin result before confirmation
  const [pendingResult, setPendingResult] = useState<string | null>(null);
  const [isSpinning, setIsSpinning] = useState(false);
  const [targetChallengeIndex, setTargetChallengeIndex] = useState<number | undefined>(undefined);

  // Run tracking state
  const [showHistory, setShowHistory] = useState(false);
  const [runs, setRuns] = useState<Run[]>([]);
  const [currentRunId, setCurrentRunId] = useState<string | null>(null);

  // Load runs on mount
  useEffect(() => {
    setRuns(getRuns());
  }, []);

  const startFlow = () => {
    setRerollsLeft(config.rerolls);
    setStep("CLASS");
    setPendingResult(null);
  };

  // --- Logic Helpers ---

  const getWeightedChallengeIndex = (availableChallenges: Challenge[]): number => {
    const totalWeight = availableChallenges.reduce((sum, c) => sum + c.weight, 0);
    let random = Math.random() * totalWeight;

    for (let i = 0; i < availableChallenges.length; i++) {
      random -= availableChallenges[i].weight;
      if (random <= 0) return i;
    }
    return 0;
  };

  const prepareChallengeSpin = () => {
    const available = CHALLENGES.filter(c => !selections.challenges.find(sc => sc.id === c.id));
    // If no challenges left, skip
    if (available.length === 0) {
      setStep("RESULT");
      return;
    }
    const index = getWeightedChallengeIndex(available);
    setTargetChallengeIndex(index);
  };

  // --- Handlers ---

  const handleSpinComplete = (result: string) => {
    setPendingResult(result);
    setIsSpinning(false);
  };

  const confirmSelection = () => {
    if (!pendingResult) return;

    if (step === "CLASS") {
      setSelections(prev => ({ ...prev, className: pendingResult as ClassName }));
      setPendingResult(null);
      setStep("BUILD");
    } else if (step === "BUILD") {
      setSelections(prev => ({ ...prev, build: pendingResult }));
      setPendingResult(null);
      if (config.challengeCount > 0) {
        prepareChallengeSpin();
        setStep("CHALLENGE");
      } else {
        setStep("RESULT");
      }
    } else if (step === "CHALLENGE") {
      const challenge = CHALLENGES.find(c => c.text === pendingResult);
      if (challenge) {
        setSelections(prev => ({
          ...prev,
          challenges: [...prev.challenges, challenge]
        }));
      }
      setPendingResult(null);

      // Check if we need more challenges
      // Note: We just added one to state, but state update is async.
      // However, we can check current length + 1
      if (selections.challenges.length + 1 < config.challengeCount) {
        // Prepare next spin
        // We need to briefly reset the wheel or just update the target
        // To force a re-render of the wheel or reset its state, we might need a key or similar.
        // For now, let's just call prepareChallengeSpin.
        // But we need to wait for state update?
        // Let's use a timeout to allow state to settle, then prepare next.
        setTimeout(() => {
          prepareChallengeSpin();
          // We stay on "CHALLENGE" step, but we need to reset pendingResult (done above)
        }, 100);
      } else {
        setStep("RESULT");
      }
    }
  };

  const useReroll = () => {
    if (rerollsLeft > 0) {
      setRerollsLeft(prev => prev - 1);
      setPendingResult(null);
      // If we are in CHALLENGE step, we need to pick a new target index
      if (step === "CHALLENGE") {
        prepareChallengeSpin();
      }
    }
  };

  const reset = () => {
    setStep("CONFIG");
    setSelections({ className: null, build: null, challenges: [] });
    setPendingResult(null);
    setCurrentRunId(null);
  };

  // Run tracking handlers
  const handleStartRun = () => {
    if (!selections.className || !selections.build) return;

    const run = saveRun({
      className: selections.className,
      build: selections.build,
      challenges: selections.challenges,
      status: 'active'
    });
    setCurrentRunId(run.id);
    setRuns(getRuns());
  };

  const handleUpdateStatus = (id: string, status: Run['status']) => {
    updateRunStatus(id, status);
    setRuns(getRuns());
  };

  const handleDeleteRun = (id: string) => {
    deleteRun(id);
    setRuns(getRuns());
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      importRuns(file).then(() => {
        setRuns(getRuns());
        alert('Runs imported successfully!');
      }).catch(() => {
        alert('Error importing runs');
      });
    }
  };

  // --- Render Helpers ---

  // Generate options for challenge count dropdown
  const challengeOptions = Array.from({ length: 6 }, (_, i) => i); // 0 to 5

  return (
    <main className={styles.main}>
      <div className={styles.backgroundLayer} />
      <div className={styles.fireOverlayBack} />
      <div className={styles.fireOverlay} />
      {/* Visual Effects */}
      <div className="blood-splatter" style={{ top: '10%', left: '5%', width: '300px', height: '300px' }} />
      <div className="blood-splatter" style={{ bottom: '15%', right: '10%', width: '400px', height: '400px', animationDelay: '1s' }} />

      <h1 className={`${styles.title} ${step !== "CONFIG" ? styles.titleFixed : ""}`}>GHEED'S GAMBLE</h1>

      {/* Progress Panel */}
      {step !== "CONFIG" && (
        <div className={styles.progressPanel}>
          <div className={styles.stat}>
            <span className={styles.label}>Rerolls:</span>
            <span className={styles.value}>{rerollsLeft}</span>
          </div>
          <div className={styles.selections}>
            {selections.className && <div>{selections.className}</div>}
            {selections.build && <div>{selections.build}</div>}
            {selections.challenges.map(c => <div key={c.id} className={styles.challengeItem}>{c.text}</div>)}
          </div>
        </div>
      )}

      {step === "CONFIG" && (
        <section className={styles.configContainer} aria-labelledby="config-heading">
          <h2 id="config-heading">CONFIGURE YOUR RUN</h2>
          <div className={styles.configGroup}>
            <label htmlFor="rerolls-input">Rerolls Allowed:</label>
            <input
              id="rerolls-input"
              type="number"
              min="0"
              max="10"
              value={config.rerolls}
              onChange={(e) => setConfig({ ...config, rerolls: parseInt(e.target.value) || 0 })}
              aria-label="Number of rerolls allowed"
              aria-describedby="rerolls-desc"
            />
            <span id="rerolls-desc" className="sr-only">Set the number of times you can reroll your fate</span>
          </div>
          <div className={styles.configGroup}>
            <label htmlFor="challenges-select">Challenges:</label>
            <select
              id="challenges-select"
              value={config.challengeCount}
              onChange={(e) => setConfig({ ...config, challengeCount: parseInt(e.target.value) })}
              aria-label="Number of challenge modifiers"
            >
              <option value={0}>None (Coward)</option>
              <option value={1}>1 (Cautious)</option>
              <option value={2}>2 (Brave)</option>
              <option value={3}>3 (Reckless)</option>
              <option value={4}>4 (Insane)</option>
              <option value={5}>5 (Death Wish)</option>
            </select>
          </div>
          <button
            onClick={startFlow}
            className={styles.startButton}
            aria-label="Start the randomizer and enter the darkness"
          >
            ENTER THE DARKNESS
          </button>
          <button
            onClick={() => setShowHistory(true)}
            className={styles.historyButton}
            aria-label="View your run history"
          >
            VIEW RUN HISTORY
          </button>
        </section>
      )}

      {/* Steps with Wheel */}
      {(step === "CLASS" || step === "BUILD" || step === "CHALLENGE") && (
        <div className={styles.stepContainer}>
          <h2>
            {step === "CLASS" && "FATE: CHOOSE YOUR CLASS"}
            {step === "BUILD" && `FATE: CHOOSE YOUR BUILD (${selections.className})`}
            {step === "CHALLENGE" && `FATE: CHOOSE CHALLENGE ${selections.challenges.length + 1}/${config.challengeCount}`}
          </h2>

          {!pendingResult ? (
            <Wheel
              key={`${step}-${selections.challenges.length}`} // Force remount on step change or challenge count change
              items={
                step === "CLASS" ? CLASSES :
                  (step === "BUILD" && selections.className) ? BUILDS[selections.className].map(b => b.name) :
                    CHALLENGES.map(c => c.text)
              }
              winningIndex={step === "CHALLENGE" ? targetChallengeIndex : undefined}
              onSpinComplete={handleSpinComplete}
            />
          ) : (
            <div className={styles.pendingResult}>
              <h3>FATE HAS CHOSEN:</h3>
              <div className={styles.resultValue}>{pendingResult}</div>

              {/* Show Description if it's a Build */}
              {step === "BUILD" && selections.className && (
                <div className={styles.description}>
                  {(selections.className && BUILDS[selections.className]) ?
                    BUILDS[selections.className].find(b => b.name === pendingResult)?.description
                    : ""}
                </div>
              )}

              {/* Show Description if it's a Challenge */}
              {step === "CHALLENGE" && (
                <div className={styles.description}>
                  {CHALLENGES.find(c => c.text === pendingResult)?.description}
                </div>
              )}

              <div className={styles.actions}>
                <button
                  onClick={confirmSelection}
                  className={styles.confirmButton}
                  aria-label="Accept the selected fate and continue"
                >
                  ACCEPT FATE
                </button>
                <button
                  onClick={useReroll}
                  disabled={rerollsLeft === 0}
                  className={styles.rerollButton}
                  aria-label={`Reroll your fate, ${rerollsLeft} rerolls remaining`}
                  aria-disabled={rerollsLeft === 0}
                >
                  DEFY FATE (Reroll: {rerollsLeft})
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {step === "RESULT" && (
        <div className={styles.resultCard}>
          <h2 className={styles.resultTitle}>YOUR CONTRACT IS SEALED</h2>
          <div className={styles.resultDetails}>
            <p><strong>CLASS:</strong> <span>{selections.className}</span></p>
            <p><strong>BUILD:</strong> <span>{selections.build}</span></p>
            {selections.className && selections.build && (
              <p className={styles.summaryDescription}>
                <em>{(selections.className && BUILDS[selections.className]) ?
                  BUILDS[selections.className].find(b => b.name === selections.build)?.description
                  : ""}</em>
              </p>
            )}
            <p><strong>CHALLENGES:</strong></p>
            <ul>
              {selections.challenges.length === 0 ? <li>None</li> : selections.challenges.map(c => (
                <li key={c.id}>
                  <strong>{c.text}</strong>: {c.description}
                </li>
              ))}
            </ul>
          </div>
          <div className={styles.actions}>
            {!currentRunId ? (
              <button
                onClick={handleStartRun}
                className={styles.startRunButton}
                aria-label="Start tracking this run in your history"
              >
                START RUN
              </button>
            ) : (
              <div className={styles.runStatus} role="status" aria-live="polite">
                ✓ Run Started - Track in History
              </div>
            )}
            <button
              onClick={reset}
              aria-label="Reset and create a new randomized run"
            >
              NEW RUN
            </button>
          </div>
        </div>
      )}

      {/* History Modal */}
      {showHistory && (
        <div
          className={styles.modalOverlay}
          onClick={() => setShowHistory(false)}
          role="dialog"
          aria-modal="true"
          aria-labelledby="history-modal-title"
        >
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2 id="history-modal-title">RUN HISTORY</h2>
              <button
                onClick={() => setShowHistory(false)}
                className={styles.closeButton}
                aria-label="Close run history modal"
              >
                ×
              </button>
            </div>
            <div className={styles.modalActions}>
              <button
                onClick={exportRuns}
                className={styles.exportButton}
                aria-label="Export your run history as a JSON file"
              >
                EXPORT
              </button>
              <label className={styles.importButton}>
                IMPORT
                <input
                  type="file"
                  accept=".json"
                  onChange={handleImport}
                  style={{ display: 'none' }}
                  aria-label="Import run history from a JSON file"
                />
              </label>
            </div>
            <div className={styles.runList}>
              {runs.length === 0 ? (
                <p className={styles.emptyState}>No runs yet. Complete a run to see it here!</p>
              ) : (
                runs.map(run => (
                  <div key={run.id} className={styles.runItem}>
                    <div className={styles.runHeader}>
                      <span className={`${styles.statusBadge} ${styles[run.status]}`}>
                        {run.status.toUpperCase()}
                      </span>
                      <span className={styles.runDate}>
                        {new Date(run.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                    <div className={styles.runDetails}>
                      <p><strong>{run.className}</strong> - {run.build}</p>
                      {run.challenges.length > 0 && (
                        <p className={styles.challengesList}>
                          {run.challenges.map(c => c.text).join(', ')}
                        </p>
                      )}
                    </div>
                    <div className={styles.runActions}>
                      {run.status === 'active' && (
                        <>
                          <button onClick={() => handleUpdateStatus(run.id, 'completed')} className={styles.completeButton}>
                            ✓ Complete
                          </button>
                          <button onClick={() => handleUpdateStatus(run.id, 'failed')} className={styles.failButton}>
                            ✗ Failed
                          </button>
                        </>
                      )}
                      <button onClick={() => handleDeleteRun(run.id)} className={styles.deleteButton}>
                        Delete
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
