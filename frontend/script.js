const form = document.getElementById("redeem-form");
const input = document.getElementById("code-input");
const message = document.getElementById("message");

form.addEventListener("submit", async (e) => {
  e.preventDefault(); // stops page refresh

  const code = input.value.trim();
  message.textContent = "";

  try {
    const res = await fetch("http://127.0.0.1:8000/giftcards/redeem", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code }),
    });

    const data = await res.json();

    if (!res.ok) {
      if (res.status === 404) {
        message.textContent = "❌ Invalid gift card";
      } else if (res.status === 400) {
        message.textContent = "❌ Gift card already redeemed";
      } else if (res.status === 429) {
        message.textContent = "⏳ Too many attempts. Please wait.";
      } else {
        message.textContent = "⚠️ Server error";
      }
      return;
    }

    message.textContent = `🎉 Redeemed £${data.value} ${data.currency}`;
  } catch (err) {
    message.textContent = "⚠️ Network error";
  }
});
