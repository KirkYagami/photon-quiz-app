class QuizTimer {
    constructor(totalSeconds, displayElementId, onExpireCallback, storageKey = 'quizTimer') {
        this.totalSeconds = totalSeconds;
        this.displayElement = document.getElementById(displayElementId);
        this.onExpireCallback = onExpireCallback;
        this.intervalId = null;
        this.isRunning = false;
        this.storageKey = storageKey;
        
        // Restore from sessionStorage if exists
        this.restoreState();
    }

    restoreState() {
        const saved = sessionStorage.getItem(this.storageKey);
        if (saved) {
            const data = JSON.parse(saved);
            this.remainingSeconds = data.remainingSeconds;
            this.totalSeconds = data.totalSeconds;
        } else {
            this.remainingSeconds = this.totalSeconds;
        }
    }

    saveState() {
        const data = {
            remainingSeconds: this.remainingSeconds,
            totalSeconds: this.totalSeconds
        };
        sessionStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.updateDisplay();
        
        this.intervalId = setInterval(() => {
            this.remainingSeconds--;
            this.saveState(); // Save state every second
            this.updateDisplay();
            
            // Warning at 5 minutes
            if (this.remainingSeconds === 300) {
                this.showWarning('5 minutes remaining!');
            }
            
            // Warning at 1 minute
            if (this.remainingSeconds === 60) {
                this.showWarning('1 minute remaining!');
            }
            
            // Timer expired
            if (this.remainingSeconds <= 0) {
                this.stop();
                this.clearState(); // Clear storage when done
                this.showWarning('Time is up! Submitting quiz...');
                
                if (this.onExpireCallback) {
                    setTimeout(() => {
                        this.onExpireCallback();
                    }, 2000);
                }
            }
        }, 1000);
    }

    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
            this.isRunning = false;
            this.saveState(); // Save when stopping
        }
    }

    clearState() {
        sessionStorage.removeItem(this.storageKey);
    }

    updateDisplay() {
        const minutes = Math.floor(this.remainingSeconds / 60);
        const seconds = this.remainingSeconds % 60;
        const timeString = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        
        if (this.displayElement) {
            this.displayElement.textContent = timeString;
            
            // Change color based on remaining time
            const timerElement = this.displayElement.parentElement;
            if (this.remainingSeconds <= 60) {
                timerElement.style.color = '#e74c3c';
                timerElement.style.fontWeight = 'bold';
            } else if (this.remainingSeconds <= 300) {
                timerElement.style.color = '#f39c12';
            }
        }
    }

    showWarning(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-error';
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '20px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.minWidth = '300px';
        alertDiv.style.textAlign = 'center';
        alertDiv.textContent = message;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    reset() {
        this.stop();
        this.remainingSeconds = this.totalSeconds;
        this.clearState();
        this.updateDisplay();
    }

    getElapsedTime() {
        return this.totalSeconds - this.remainingSeconds;
    }

    getFormattedElapsedTime() {
        const elapsed = this.getElapsedTime();
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        return `${minutes}m ${seconds}s`;
    }
}