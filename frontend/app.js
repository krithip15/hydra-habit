const API_BASE_URL = "";

let currentUserId = null;

/* -----------------------------
   DOM ELEMENTS
----------------------------- */

const userIdInput = document.getElementById("userId");

const loadUserButton = document.getElementById("loadUserButton");

const userProfile = document.getElementById("userProfile");

const hydrationDate = document.getElementById("hydrationDate");

const waterIntake = document.getElementById("waterIntake");

const addHydrationButton = document.getElementById("addHydrationButton");

const hydrationMessage = document.getElementById("hydrationMessage");

const summaryMessage = document.getElementById("summaryMessage");

const agentMessage = document.getElementById("agentMessage");

const recommendationBox = document.getElementById("recommendationBox");

const analyzeButton = document.getElementById("analyzeButton");

const recordsBox = document.getElementById("recordsBox");

/* -----------------------------
   DEFAULT DATE
----------------------------- */

hydrationDate.value = new Date().toISOString().split("T")[0];

/* -----------------------------
   LOAD USER
----------------------------- */

loadUserButton.addEventListener("click", loadUser);

async function loadUser() {
  const userId = Number(userIdInput.value);

  if (!userId) {
    showMessage(hydrationMessage, "Please enter a valid user ID.");

    return;
  }

  try {
    const response = await fetch(`/health-summary/${userId}`);

    const summary = await response.json();

    if (!response.ok) {
      showMessage(hydrationMessage, summary.detail || "User not found.");

      return;
    }

    currentUserId = userId;

    displayBasicProfile(summary);

    displaySummary(summary);

    await loadRecords();

    recommendationBox.classList.add("hidden");

    showMessage(hydrationMessage, "User loaded successfully.");
  } catch (error) {
    console.error(error);

    showMessage(hydrationMessage, "Could not connect to the API.");
  }
}

/* -----------------------------
   DISPLAY BASIC PROFILE
----------------------------- */

function displayBasicProfile(summary) {
  userProfile.classList.remove("hidden");

  userProfile.innerHTML = `

        <div class="profile-item">
            <span>User ID</span>
            <strong>${summary.user_id}</strong>
        </div>

        <div class="profile-item">
            <span>Daily target</span>
            <strong>${summary.target_ml} ml</strong>
        </div>

        <div class="profile-item">
            <span>Current status</span>
            <strong>${formatStatus(summary.target_status)}</strong>
        </div>

    `;
}

/* -----------------------------
   ADD HYDRATION
----------------------------- */

addHydrationButton.addEventListener("click", addHydration);

async function addHydration() {
  if (!currentUserId) {
    showMessage(hydrationMessage, "Load a user first.");

    return;
  }

  const intake = Number(waterIntake.value);

  const selectedDate = hydrationDate.value;

  if (!selectedDate) {
    showMessage(hydrationMessage, "Please select a date.");

    return;
  }

  if (Number.isNaN(intake) || intake < 0) {
    showMessage(hydrationMessage, "Please enter a valid intake amount.");

    return;
  }

  try {
    const response = await fetch("/health-data", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        user_id: currentUserId,

        date: selectedDate,

        water_intake_ml: intake,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage(
        hydrationMessage,
        data.detail || "Could not save hydration record.",
      );

      return;
    }

    showMessage(hydrationMessage, "Hydration record saved.");

    waterIntake.value = "";

    await loadRecords();

    await loadSummary();
  } catch (error) {
    console.error(error);

    showMessage(hydrationMessage, "Could not connect to the API.");
  }
}

/* -----------------------------
   LOAD HYDRATION RECORDS
----------------------------- */

async function loadRecords() {
  if (!currentUserId) {
    return;
  }

  try {
    const response = await fetch(`/health-data/${currentUserId}`);

    const records = await response.json();

    if (!response.ok) {
      recordsBox.innerHTML = `
                <p class="empty-state">
                    Could not load hydration records.
                </p>
            `;

      return;
    }

    if (records.length === 0) {
      recordsBox.innerHTML = `
                <p class="empty-state">
                    No hydration records found.
                </p>
            `;

      return;
    }

    const rows = records
      .map((record) => {
        return `
                    <tr>

                        <td>
                            ${formatDate(record.date)}
                        </td>

                        <td>
                            <strong>
                                ${record.water_intake_ml} ml
                            </strong>
                        </td>

                        <td class="record-status">
                            Stored
                        </td>

                    </tr>
                `;
      })
      .join("");

    recordsBox.innerHTML = `

            <table class="records-table">

                <thead>

                    <tr>
                        <th>Date</th>
                        <th>Intake</th>
                        <th>Status</th>
                    </tr>

                </thead>

                <tbody>
                    ${rows}
                </tbody>

            </table>

        `;
  } catch (error) {
    console.error(error);

    recordsBox.innerHTML = `
            <p class="empty-state">
                Could not connect to the API.
            </p>
        `;
  }
}

/* -----------------------------
   LOAD SUMMARY
----------------------------- */

async function loadSummary() {
  if (!currentUserId) {
    return;
  }

  try {
    const response = await fetch(`/health-summary/${currentUserId}`);

    const summary = await response.json();

    if (!response.ok) {
      showMessage(summaryMessage, summary.detail || "Could not load summary.");

      return;
    }

    displaySummary(summary);
  } catch (error) {
    console.error(error);

    showMessage(summaryMessage, "Could not load summary.");
  }
}

/* -----------------------------
   DISPLAY SUMMARY
----------------------------- */

function displaySummary(summary) {
  document.getElementById("targetValue").textContent =
    `${summary.target_ml} ml`;

  document.getElementById("averageValue").textContent =
    summary.average_intake_ml === null
      ? "—"
      : `${summary.average_intake_ml} ml`;

  document.getElementById("achievementValue").textContent =
    summary.target_achievement_percent === null
      ? "—"
      : `${summary.target_achievement_percent}%`;

  document.getElementById("gapValue").textContent =
    summary.gap_ml === null ? "—" : `${summary.gap_ml} ml`;

  document.getElementById("trendValue").textContent = formatStatus(
    summary.trend,
  );

  document.getElementById("qualityValue").textContent = formatStatus(
    summary.data_quality,
  );

  showMessage(
    summaryMessage,
    `Valid days: ${summary.valid_days} · Missing days: ${summary.missing_days} · Suspicious days: ${summary.suspicious_days}`,
  );
}

/* -----------------------------
   RUN AGENT
----------------------------- */

analyzeButton.addEventListener("click", analyzeHydration);

async function analyzeHydration() {
  if (!currentUserId) {
    showMessage(agentMessage, "Load a user first.");

    return;
  }

  analyzeButton.disabled = true;

  analyzeButton.textContent = "Analyzing...";

  try {
    const response = await fetch(`/agent/analyze/${currentUserId}`, {
      method: "POST",
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage(agentMessage, data.detail || "Agent analysis failed.");

      return;
    }

    document.getElementById("insightText").textContent = data.insight;

    document.getElementById("recommendationText").textContent =
      data.recommendation;

    document.getElementById("actionText").textContent = formatStatus(
      data.action,
    );

    document.getElementById("confidenceText").textContent = formatStatus(
      data.confidence,
    );

    recommendationBox.classList.remove("hidden");

    showMessage(
      agentMessage,
      `Analysis completed · Recommendation #${data.recommendation_id}`,
    );
  } catch (error) {
    console.error(error);

    showMessage(agentMessage, "Could not connect to the API.");
  } finally {
    analyzeButton.disabled = false;

    analyzeButton.textContent = "Analyze My Hydration";
  }
}

/* -----------------------------
   HELPERS
----------------------------- */

function formatStatus(value) {
  if (!value) {
    return "—";
  }

  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`);

  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function showMessage(element, message) {
  element.textContent = message;
}
