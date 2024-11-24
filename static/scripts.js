let uploadedFilePath = '';

async function uploadVideo() {
    const videoInput = document.getElementById('video-upload');
    const file = videoInput.files[0];
    if (!file) {
        alert('Please select a video file to upload.');
        return;
    }

    const formData = new FormData();
    formData.append('video', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    if (response.ok) {
        uploadedFilePath = data.file_path;
        alert('Video uploaded successfully!');
    } else {
        alert(data.error || 'Failed to upload video.');
    }
}

async function editVideo() {
    const action = document.getElementById('action').value;
    const text = document.getElementById('overlay-text').value;
    const start = parseFloat(document.getElementById('start-trim').value);
    const end = parseFloat(document.getElementById('end-trim').value);

    if (!uploadedFilePath) {
        alert('Please upload a video first.');
        return;
    }

    const response = await fetch('/edit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: uploadedFilePath,
            action: action,
            text: text,
            start: start,
            end: end
        })
    });

    const data = await response.json();
    if (response.ok) {
        alert('Video processed successfully!');
        uploadedFilePath = data.output_path;
    } else {
        alert(data.error || 'Failed to process video.');
    }
}

function downloadVideo() {
    if (!uploadedFilePath) {
        alert('Please process a video first.');
        return;
    }

    const filename = uploadedFilePath.split('/').pop();
    window.location.href = `/download/${filename}`;
}
