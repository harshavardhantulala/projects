document.getElementById("fileForm").onsubmit = async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const hashInput = document.getElementById("hashInput").value.trim();
    const resultDiv = document.getElementById("result");

    if (fileInput.files.length === 0) {
        resultDiv.textContent = "Please upload a file.";
        return;
    }

    const file = fileInput.files[0];

    // Create FormData and append file/hash
    const formData = new FormData();
    formData.append("file", file);
    formData.append("hash", hashInput);

    try {
        const response = await fetch("/check", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const result = await response.json();

        if (result.isAuthentic) {
            resultDiv.textContent = "File is authentic! ✅";
            resultDiv.style.color = "green";
        } else {
            resultDiv.textContent = "File is NOT authentic! ❌";
            resultDiv.style.color = "red";
        }
    } catch (error) {
        console.error(error);
        resultDiv.textContent = "An error occurred. Please try again.";
        resultDiv.style.color = "red";
    }
};
