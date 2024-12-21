// app/static/js/main.js
document.getElementById("resumeForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const submitButton = e.target.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  submitButton.innerHTML = "Generating...";

  // Hide any existing messages
  document.getElementById("downloadSection").style.display = "none";
  document.getElementById("errorSection").style.display = "none";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        full_name: document.getElementById("fullName").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        linkedin: document.getElementById("linkedin").value,
        github: document.getElementById("github").value,
        background: document.getElementById("background").value,
        role: document.getElementById("role").value,
        responsibilities: document.getElementById("responsibilities").value,
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      document.getElementById("downloadSection").style.display = "block";
    } else {
      document.getElementById("errorMessage").textContent = data.message;
      document.getElementById("errorSection").style.display = "block";
    }
  } catch (error) {
    document.getElementById("errorMessage").textContent =
      "An error occurred. Please try again.";
    document.getElementById("errorSection").style.display = "block";
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = "Generate Resume";
  }
});
