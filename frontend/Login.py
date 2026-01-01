const login = async (email, password) => {
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const res = await fetch("http://localhost:8000/auth/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  const data = await res.json();
  localStorage.setItem("token", data.access_token);
};
