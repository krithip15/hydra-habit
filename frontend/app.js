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
const summaryWindowLabel = document.getElementById("summaryWindowLabel");

const agentTrace = document.getElementById("agentTrace");
const traceSteps = document.getElementById("traceSteps");

/* -----------------------------
   DEFAULT DATE
----------------------------- */

const today = new Date().toISOString().split("T")[0];

hydrationDate.value = today;
hydrationDate.max = today;

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
    const userResponse = await fetch(`/users/${userId}`);

    const user = await userResponse.json();

    if (!userResponse.ok) {
      showMessage(hydrationMessage, user.detail || "User not found.");

      return;
    }

    currentUserId = userId;

    displayUserProfile(user);

    await loadRecords();
    await loadSummary();

    recommendationBox.classList.add("hidden");
    agentTrace.classList.add("hidden");

    showMessage(hydrationMessage, "User loaded successfully.");
  } catch (error) {
    console.error(error);

    showMessage(hydrationMessage, "Could not connect to the API.");
  }
}

/* -----------------------------
   DISPLAY USER PROFILE
----------------------------- */

function displayUserProfile(user) {
  userProfile.classList.remove("hidden");

  userProfile.innerHTML = `

        <div class="profile-item">
            <span>Name</span>
            <strong>${escapeHtml(user.name)}</strong>
        </div>

        <div class="profile-item">
            <span>Age</span>
            <strong>${user.age}</strong>
        </div>

        <div class="profile-item">
            <span>Gender</span>
            <strong>${escapeHtml(user.gender)}</strong>
        </div>

        <div class="profile-item">
            <span>Height</span>
            <strong>${user.height_cm} cm</strong>
        </div>

        <div class="profile-item">
            <span>Weight</span>
            <strong>${user.weight_kg} kg</strong>
        </div>

        <div class="profile-item">
            <span>Health goal</span>
            <strong>${formatStatus(user.health_goal)}</strong>
        </div>

        <div class="profile-item">
            <span>Daily target</span>
            <strong>${user.daily_water_target_ml} ml</strong>
        </div>

        <div class="profile-item">
            <span>Reminder time</span>
            <strong>${user.preferred_reminder_time || "Not set"}</strong>
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

  if (selectedDate > today) {
    showMessage(hydrationMessage, "Hydration date cannot be in the future.");

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

      summaryWindowLabel.classList.add("hidden");

      return;
    }

    summaryWindowLabel.classList.remove("hidden");

    const todayDate = new Date();

    todayDate.setHours(0, 0, 0, 0);

    const startDate = new Date(todayDate);

    startDate.setDate(todayDate.getDate() - 6);

    const rows = records
      .map((record) => {
        const recordDate = new Date(`${record.date}T00:00:00`);

        const isInSummaryWindow =
          recordDate >= startDate && recordDate <= todayDate;

        return `
                        <tr class="${isInSummaryWindow ? "summary-row" : ""}">

                            <td>
                                ${formatDate(record.date)}
                            </td>

                            <td>
                                <strong>
                                    ${record.water_intake_ml} ml
                                </strong>
                            </td>

                            <td>

                                ${
                                  isInSummaryWindow
                                    ? `
                                            <span class="summary-status">
                                                IN SUMMARY
                                            </span>
                                          `
                                    : `
                                            <span class="older-status">
                                                Older record
                                            </span>
                                          `
                                }

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
    `Valid days: ${summary.valid_days} · ` +
      `Missing days: ${summary.missing_days} · ` +
      `Suspicious days: ${summary.suspicious_days}`,
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

  agentTrace.classList.add("hidden");

  try {
    const response = await fetch(`/agent/analyze/${currentUserId}`, {
      method: "POST",
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage(agentMessage, data.detail || "Agent analysis failed.");

      return;
    }

    /*
     * The normal recommendation path
     * returns insight + recommendation.
     */
    if (data.insight && data.insight.trim()) {
      document.getElementById("insightText").textContent = data.insight;

      document.getElementById("recommendationText").textContent =
        data.recommendation || "No recommendation provided.";

      document.getElementById("actionText").textContent = formatStatus(
        data.action,
      );

      document.getElementById("confidenceText").textContent = formatStatus(
        data.confidence,
      );

      recommendationBox.classList.remove("hidden");
    } else {
      /*
       * NO_ACTION / insufficient-data case.
       *
       * The analysis completed but there
       * may not be a normal recommendation
       * returned by the endpoint.
       */
      recommendationBox.classList.remove("hidden");

      document.getElementById("insightText").textContent =
        "There is not enough reliable hydration data to make a meaningful recommendation.";

      document.getElementById("recommendationText").textContent =
        "Continue recording your daily water intake so there is enough reliable data for analysis.";

      document.getElementById("actionText").textContent = "No Action";

      document.getElementById("confidenceText").textContent = "High";
    }

    showMessage(
      agentMessage,
      `Analysis completed · Recommendation #${data.recommendation_id}`,
    );

    await loadAgentTrace();
  } catch (error) {
    console.error(error);

    showMessage(agentMessage, "Could not connect to the API.");
  } finally {
    analyzeButton.disabled = false;

    analyzeButton.textContent = "Analyze My Hydration";
  }
}

/* -----------------------------
   LOAD AGENT TRACE
----------------------------- */

async function loadAgentTrace() {
  if (!currentUserId) {
    return;
  }

  try {
    const response = await fetch(`/agent/logs/${currentUserId}`);

    const logs = await response.json();

    if (!response.ok || !Array.isArray(logs) || logs.length === 0) {
      agentTrace.classList.add("hidden");

      return;
    }

    const latestRun = getLatestRun(logs);

    /*
     * API returns newest first.
     * Reverse the selected run so that
     * the UI shows execution order.
     */
    const orderedLogs = [...latestRun].reverse();

    const stepNames = {
      get_user_profile: "User profile retrieved",

      get_hydration_summary: "Hydration summary calculated",

      check_data_quality: "Data quality checked",

      llm_analyze: "AI recommendation generated",

      save_recommendation: "Recommendation saved",
    };

    traceSteps.innerHTML = orderedLogs
      .map((log, index) => {
        const label = stepNames[log.tool_name] || formatStatus(log.tool_name);

        return `

                        <div class="trace-step">

                            <div class="trace-icon">
                                ✓
                            </div>

                            <span>
                                ${escapeHtml(label)}
                            </span>

                            <small>
                                Step ${index + 1}
                            </small>

                        </div>

                    `;
      })
      .join("");

    agentTrace.classList.remove("hidden");
  } catch (error) {
    console.error(error);

    agentTrace.classList.add("hidden");
  }
}

/* -----------------------------
   GET LATEST AGENT RUN
----------------------------- */

function getLatestRun(logs) {
  const expectedSteps = [
    "get_user_profile",
    "get_hydration_summary",
    "check_data_quality",
    "llm_analyze",
    "save_recommendation",
  ];

  return logs
    .filter((log) => expectedSteps.includes(log.tool_name))
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 5);
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

function escapeHtml(value) {
  const div = document.createElement("div");

  div.textContent = value ?? "";

  return div.innerHTML;
}

function showMessage(element, message) {
  element.textContent = message;
}
