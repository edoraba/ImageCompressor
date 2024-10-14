document.getElementById('imageForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const imageFile = document.getElementById('imageFile').files[0];
    const maxSize = document.getElementById('maxSize').value;
    const quality = document.getElementById('quality').value;

    if (!imageFile) {
        alert("Please select an image");
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('max_size', maxSize);
    formData.append('quality', quality);

    try {
        const response = await fetch('/compress', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            console.log('Image compressed successfully');
            const blob = await response.blob();
            const downloadUrl = URL.createObjectURL(blob);

            // Crea un link temporaneo per scaricare il file automaticamente
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = 'compressed_image.webp';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            // Verifica se l'immagine viene scaricata correttamente
            console.log('Download link triggered:', downloadUrl);
        } else {
            console.error('Error compressing image');
            alert('Error compressing image');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
