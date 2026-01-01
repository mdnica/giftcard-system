const redeemGiftCard = async (code) => {
  const token = localStorage.getItem("token");

  const res = await fetch("http://localhost:8000/giftcards/redeem", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({ code }),
  });

  return await res.json();
};
