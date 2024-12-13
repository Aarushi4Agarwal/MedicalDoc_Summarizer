document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("fileInput");
            // const textInput = document.getElementById('textInput').value;
            const file = fileInput.files[0];
 
            if (!file) {
                alert('Please select a file to upload');
                return;
            }
 
            // Create a FormData object to send data
            const formData = new FormData();
            formData.append('file', file);
            // formData.append('textInput', textInput);
 
            try {
                document.getElementById('summaryDisplay').textContent = "Waiting for response...";
                // Send the form data to the server using fetch API
                console.log("making the request")
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
 
                // Check if the upload was successful
                if (!response.ok) {
                    throw new Error(response);
                }
 
                // Get the response from the server
                const responseData = await response.text();
 
                // Display the response
                console.log(responseData)
                document.getElementById('summaryDisplay').textContent = responseData;
 
            } catch (error) {
                console.log(error)
                document.getElementById('summaryDisplay').textContent = `Error: ${error.message}`;
            }
});

