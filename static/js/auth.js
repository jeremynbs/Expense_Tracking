// Code Function: Final Project
// Date: 2025/05/27, created by: 蕭智強

function handleCredentialResponse(response) {
  const id_token = response.credential;

  // Send the token to Flask backend
  fetch("/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id_token }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        alert("Login failed: " + data.error);
      } else {
        window.location.href = "/"; // Redirect to dashboard on success
      }
    })
    .catch((err) => {
      console.error("Login error:", err);
    });
}

// Load Google Identity script and render the button
window.onload = function () {
  google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: handleCredentialResponse,
  });

  google.accounts.id.renderButton(
    document.getElementById("google-login"),
    { theme: "outline", size: "large" }
  );
};
