// Function to handle the "Download" button click
document.getElementById('download-btn').addEventListener('click', function () {
    // Get the video URL and selected quality
    const videoUrl = document.getElementById('video-url').value.trim();
    const quality = document.getElementById('quality').value;

    // Validate the input
    if (!videoUrl) {
        alert("Please enter a valid YouTube URL!");
        return;
    }

    // Show the loading animation
    document.getElementById('loader').style.display = 'block';

    // Send the video URL and quality to the backend
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl, quality: quality }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Failed to process the video. Please try again.');
            }
            return response.blob(); // Get the video file as a blob
        })
        .then((blob) => {
            // Create a download link for the video
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);

            // Set the appropriate file name and extension
            const extension = quality === '4k' ? 'mkv' : 'mp4';
            link.download = `video.${extension}`;

            // Simulate a click on the link to trigger download
            link.click();
        })
        .catch((error) => {
            alert(`Error: ${error.message}`);
        })
        .finally(() => {
            // Hide the loading animation
            document.getElementById('loader').style.display = 'none';
        });
});
