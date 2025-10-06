const apiBase = "";

async function postJSON(path, body) {
  const res = await fetch(`${apiBase}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  let data;
  try {
    data = await res.json();
  } catch (_) {
    data = {};
  }
  return { ok: res.ok, status: res.status, data };
}

async function getJSON(path) {
  const res = await fetch(`${apiBase}${path}`);
  let data;
  try {
    data = await res.json();
  } catch (_) {
    data = {};
  }
  return { ok: res.ok, status: res.status, data };
}

// Toggle UI
const registerSection = document.getElementById("registerSection");
const loginSection = document.getElementById("loginSection");
document.getElementById("showRegister").addEventListener("click", () => {
  registerSection.style.display = "block";
  loginSection.style.display = "none";
});
document.getElementById("showLogin").addEventListener("click", () => {
  loginSection.style.display = "block";
  registerSection.style.display = "none";
});

// Register
document
  .getElementById("registerForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("regEmail").value.trim();
    const password = document.getElementById("regPassword").value;
    const height = Number(document.getElementById("regHeight").value);
    const weight = Number(document.getElementById("regWeight").value);
    const out = document.getElementById("registerResult");
    out.textContent = "جارٍ المعالجة...";
    const { ok, data } = await postJSON("/api/register", {
      email,
      password,
      height,
      weight,
    });
    if (ok) {
      out.textContent = "تم التسجيل بنجاح";
      document.getElementById("registerForm").reset();
    } else {
      out.textContent = data.error || "فشل التسجيل";
    }
  });

// Login
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value;
  const out = document.getElementById("loginResult");
  out.textContent = "جارٍ المعالجة...";
  const { ok, data } = await postJSON("/api/login", { email, password });
  if (ok) {
    out.textContent = "تم تسجيل الدخول";
    document.getElementById("loginForm").reset();
  } else {
    out.textContent = data.error || "فشل تسجيل الدخول";
  }
});

// BMI
document.getElementById("bmiForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const height = Number(document.getElementById("bmiHeight").value);
  const weight = Number(document.getElementById("bmiWeight").value);
  const out = document.getElementById("bmiResult");
  out.textContent = "جارٍ الحساب...";
  const { ok, data } = await postJSON("/api/bmi", { height, weight });
  out.textContent = ok ? `BMI: ${data.BMI}` : data.error || "فشل الحساب";
});

// Suggestions and Meals
const mealsList = document.getElementById("mealsList");
document.getElementById("btnSuggest").addEventListener("click", async () => {
  const userId = Number(document.getElementById("suggestUserId").value);
  const out = document.getElementById("suggestResult");
  out.textContent = "جارٍ التحميل...";
  const { ok, data } = await getJSON(`/ai_suggest_meals/${userId}`);
  if (!ok) {
    out.textContent = data.error || "فشل الجلب";
    return;
  }
  out.textContent = "";
  renderMeals(data);
});

document.getElementById("btnFetchMeals").addEventListener("click", async () => {
  const type = document.getElementById("filterType").value;
  const cal = document.getElementById("filterCal").value;
  const out = document.getElementById("suggestResult");
  out.textContent = "جارٍ التحميل...";
  const q = new URLSearchParams();
  if (type) q.set("type", type);
  if (cal) q.set("max_calories", cal);
  const { ok, data } = await getJSON(`/get_meals?${q.toString()}`);
  if (!ok) {
    out.textContent = data.error || "فشل الجلب";
    return;
  }
  out.textContent = "";
  renderMeals(data);
});

async function addToHistory(mealId) {
  const userId = Number(document.getElementById("suggestUserId").value);
  const out = document.getElementById("suggestResult");
  const { ok, data } = await postJSON("/add_meal_history", {
    user_id: userId,
    meal_id: mealId,
  });
  out.textContent = ok
    ? "تمت إضافة الوجبة إلى السجل"
    : data.error || "فشل الإضافة";
}

function renderMeals(meals) {
  mealsList.innerHTML = "";
  for (const m of meals) {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${m.name}</strong> — ${m.type} — ${m.calories} kcal
      <br/><small>${m.ingredients || ""}</small>
      <div><button data-id="${m.id}">أضف للسجل</button></div>`;
    li.querySelector("button").addEventListener("click", () =>
      addToHistory(m.id)
    );
    mealsList.appendChild(li);
  }
}
