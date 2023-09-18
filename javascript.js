document.addEventListener('DOMContentLoaded', () => {
    const progressBar = document.getElementById('progressBar');
    const statusElement = document.getElementById('status');

    function updateProgress(percentage) {
        progressBar.value = percentage;
        statusElement.innerText = `${percentage}%`;
    }

    function pollProgress() {
        fetch('/get_progress')
            .then(response => response.json())
            .then(data => {
                updateProgress(data.progress);
                if (data.progress < 100) {
                    setTimeout(pollProgress, 100); // Reduced to 100 milliseconds
                }
            });
    }

    pollProgress();
});
