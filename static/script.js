// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const audioPlayer = document.getElementById('audioPlayer');
const removeBtn = document.getElementById('removeBtn');
const uploadBtn = document.getElementById('uploadBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const fullText = document.getElementById('fullText');
const segments = document.getElementById('segments');
const languageBadge = document.getElementById('languageBadge');
const timeBadge = document.getElementById('timeBadge');
const copyBtn = document.getElementById('copyBtn');
const newUploadBtn = document.getElementById('newUploadBtn');

let selectedFile = null;

// Upload area click
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    handleFile(e.dataTransfer.files[0]);
});

// Handle file selection
function handleFile(file) {
    if (!file) return;

    // Validate file type
    const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/x-m4a', 'audio/ogg', 'audio/flac', 'audio/aac'];
    const allowedExtensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac'];

    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        alert('Invalid file type. Please upload an audio file (MP3, WAV, M4A, OGG, FLAC, AAC)');
        return;
    }

    // Validate file size (300MB)
    if (file.size > 300 * 1024 * 1024) {
        alert('File size exceeds 300MB limit');
        return;
    }

    selectedFile = file;

    // Update UI
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);

    // Set audio player source
    const url = URL.createObjectURL(file);
    audioPlayer.src = url;

    // Show preview, hide upload area
    uploadArea.style.display = 'none';
    filePreview.style.display = 'block';
    resultsSection.style.display = 'none';
}

// Remove file
removeBtn.addEventListener('click', () => {
    resetUpload();
});

// Upload and transcribe
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    // Show loading
    filePreview.style.display = 'none';
    loading.style.display = 'block';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        // Hide loading
        loading.style.display = 'none';

        // Display results
        displayResults(data);

    } catch (error) {
        loading.style.display = 'none';
        alert('Error: ' + error.message);
        resetUpload();
    }
});

// Display results
function displayResults(data) {
    // Set metadata
    languageBadge.textContent = `Language: ${data.language.toUpperCase()} (${(data.language_probability * 100).toFixed(0)}%)`;
    timeBadge.textContent = `Processed in ${data.processing_time}s`;

    // Set full text
    fullText.textContent = data.full_text;

    // Clear and populate segments
    segments.innerHTML = '';
    data.segments.forEach((segment, index) => {
        const segmentDiv = document.createElement('div');
        segmentDiv.className = 'segment';
        segmentDiv.style.animationDelay = `${index * 0.05}s`;

        segmentDiv.innerHTML = `
            <div class="segment-time">${formatTime(segment.start)} → ${formatTime(segment.end)}</div>
            <div class="segment-text">${segment.text}</div>
        `;

        segments.appendChild(segmentDiv);
    });

    // Show results
    resultsSection.style.display = 'block';
}

// Copy text to clipboard
copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(fullText.textContent);

        // Visual feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 8L6 11L13 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Copied!
        `;

        setTimeout(() => {
            copyBtn.innerHTML = originalText;
        }, 2000);
    } catch (error) {
        alert('Failed to copy text');
    }
});

// New upload
newUploadBtn.addEventListener('click', () => {
    resetUpload();
});

// Reset upload state
function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    audioPlayer.src = '';
    uploadArea.style.display = 'block';
    filePreview.style.display = 'none';
    loading.style.display = 'none';
    resultsSection.style.display = 'none';
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}
