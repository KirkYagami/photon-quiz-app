class QuizTimer {
    constructor(quizId, totalMinutes, displayElementId, onExpireCallback) {
        this.quizId = quizId;
        this.totalSeconds = totalMinutes * 60;
        this.displayElement = document.getElementById(displayElementId);
        this.onExpireCallback = onExpireCallback;
        this.intervalId = null;
        this.isRunning = false;
        this.storageKey = `quiz_${quizId}_timer`;
        this.startTimeKey = `quiz_${quizId}_start_time`;
        
        // Initialize or restore state
        this.initializeTimer();
    }

    initializeTimer() {
        const startTime = localStorage.getItem(this.startTimeKey);
        
        if (startTime) {
            // Resume existing quiz
            const elapsed = Math.floor((Date.now() - parseInt(startTime)) / 1000);
            this.remainingSeconds = Math.max(0, this.totalSeconds - elapsed);
        } else {
            // Start new quiz
            this.remainingSeconds = this.totalSeconds;
            localStorage.setItem(this.startTimeKey, Date.now().toString());
        }
        
        this.updateDisplay();
    }

    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.updateDisplay();
        
        this.intervalId = setInterval(() => {
            // Recalculate from start time for accuracy
            const startTime = parseInt(localStorage.getItem(this.startTimeKey));
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            this.remainingSeconds = Math.max(0, this.totalSeconds - elapsed);
            
            this.updateDisplay();
            
            // Warnings
            if (this.remainingSeconds === 300) {
                this.showWarning('⏰ 5 minutes remaining!');
            }
            
            if (this.remainingSeconds === 60) {
                this.showWarning('⏰ 1 minute remaining!');
            }
            
            // Timer expired
            if (this.remainingSeconds <= 0) {
                this.stop();
                this.clearState();
                this.showWarning('⏰ Time is up! Submitting quiz...');
                
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
        }
    }

    clearState() {
        localStorage.removeItem(this.startTimeKey);
        localStorage.removeItem(this.storageKey);
    }

    updateDisplay() {
        const minutes = Math.floor(this.remainingSeconds / 60);
        const seconds = this.remainingSeconds % 60;
        const timeString = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        
        if (this.displayElement) {
            this.displayElement.textContent = timeString;
            
            const timerElement = this.displayElement.closest('.timer');
            if (timerElement) {
                // Change color and add warning class
                if (this.remainingSeconds <= 60) {
                    timerElement.style.color = '#e74c3c';
                    timerElement.classList.add('warning');
                } else if (this.remainingSeconds <= 300) {
                    timerElement.style.color = '#f39c12';
                    timerElement.classList.remove('warning');
                } else {
                    timerElement.style.color = '#7f8c8d';
                    timerElement.classList.remove('warning');
                }
            }
        }
    }

    showWarning(message) {
        // Remove existing warnings
        const existing = document.querySelectorAll('.timer-warning');
        existing.forEach(el => el.remove());
        
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-error timer-warning';
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '80px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.minWidth = '300px';
        alertDiv.style.textAlign = 'center';
        alertDiv.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
        alertDiv.textContent = message;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 4000);
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