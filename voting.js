document.addEventListener("DOMContentLoaded", function () {
  const responseLog = document.getElementById("responseLog");

  /**
   * Logs messages to the response log with timestamp
   * @param {string} message - The message to log
   * @param {string} type - Type of message (success, error, info)
   */
  function logResponse(message, type = "info") {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] ${message}\n`;
    responseLog.textContent += logEntry;
    responseLog.scrollTop = responseLog.scrollHeight;
  }

  /**
   * Makes API calls to the backend
   * @param {string} url - API endpoint
   * @param {string} method - HTTP method
   * @param {object} data - Data to send (optional)
   */
  async function apiCall(url, method = "GET", data = null) {
    try {
      const options = {
        method: method,
        headers: {
          "Content-Type": "application/json",
        },
      };

      if (data) {
        options.body = JSON.stringify(data);
      }

      const response = await fetch(url, options);
      return await response.json();
    } catch (error) {
      logResponse(`API Error: ${error.message}`, "error");
      return { status: "error", message: error.message };
    }
  }

  // Setup Database Tables
  document
    .getElementById("setupDatabase")
    .addEventListener("click", async function () {
      logResponse("Setting up database tables...", "info");
      const result = await apiCall("/setup-database", "POST");
      logResponse(`Database Setup: ${result.message}`, result.status);
    });

  // Add Candidate
  document
    .getElementById("addCandidate")
    .addEventListener("click", async function () {
      const name = document.getElementById("candidateName").value;
      const party = document.getElementById("candidateParty").value;
      const position = document.getElementById("candidatePosition").value;
      const description = document.getElementById("candidateDescription").value;

      if (!name || !position) {
        logResponse("Please fill in candidate name and position", "error");
        return;
      }

      const data = { name, party, position, description };
      const result = await apiCall("/add-candidate", "POST", data);
      logResponse(`Add Candidate: ${result.message}`, result.status);

      if (result.status === "success") {
        // Clear form
        document.getElementById("candidateName").value = "";
        document.getElementById("candidateParty").value = "";
        document.getElementById("candidatePosition").value = "";
        document.getElementById("candidateDescription").value = "";

        // Refresh candidates dropdown
        loadCandidatesDropdown();
      }
    });

  // Register Voter
  document
    .getElementById("registerVoter")
    .addEventListener("click", async function () {
      const voter_id = document.getElementById("voterId").value;
      const name = document.getElementById("voterName").value;
      const email = document.getElementById("voterEmail").value;

      if (!voter_id || !name || !email) {
        logResponse("Please fill in all voter registration fields", "error");
        return;
      }

      const data = { voter_id, name, email };
      const result = await apiCall("/register-voter", "POST", data);
      logResponse(`Register Voter: ${result.message}`, result.status);

      if (result.status === "success") {
        // Clear form
        document.getElementById("voterId").value = "";
        document.getElementById("voterName").value = "";
        document.getElementById("voterEmail").value = "";
      }
    });

  // Cast Vote
  document
    .getElementById("castVote")
    .addEventListener("click", async function () {
      const voter_id = document.getElementById("voteVoterId").value;
      const candidate_id = document.getElementById("voteCandidate").value;

      if (!voter_id || !candidate_id) {
        logResponse("Please enter voter ID and select a candidate", "error");
        return;
      }

      const data = { voter_id, candidate_id };
      const result = await apiCall("/cast-vote", "POST", data);
      logResponse(`Cast Vote: ${result.message}`, result.status);

      if (result.status === "success") {
        // Clear form
        document.getElementById("voteVoterId").value = "";
        document.getElementById("voteCandidate").value = "";
      }
    });

  // Load candidates into dropdown
  async function loadCandidatesDropdown() {
    const result = await apiCall("/get-candidates");
    if (result.status === "success") {
      const dropdown = document.getElementById("voteCandidate");
      dropdown.innerHTML = '<option value="">Select Candidate</option>';

      result.data.forEach((candidate) => {
        const option = document.createElement("option");
        option.value = candidate.id;
        option.textContent = `${candidate.name} - ${candidate.position} (${
          candidate.party || "Independent"
        })`;
        dropdown.appendChild(option);
      });
    }
  }

  // Get Candidates
  document
    .getElementById("getCandidates")
    .addEventListener("click", async function () {
      const result = await apiCall("/get-candidates");
      const candidatesList = document.getElementById("candidatesList");

      if (result.status === "success") {
        candidatesList.innerHTML = "";

        if (result.data.length === 0) {
          candidatesList.innerHTML = "<p>No candidates found</p>";
        } else {
          result.data.forEach((candidate) => {
            const candidateDiv = document.createElement("div");
            candidateDiv.className = "candidate-item";
            candidateDiv.innerHTML = `
                        <h4>${candidate.name} - ${candidate.position}</h4>
                        <p><strong>Party:</strong> ${
                          candidate.party || "Independent"
                        }</p>
                        <p><strong>Description:</strong> ${
                          candidate.description || "No description"
                        }</p>
                        <p><strong>Current Votes:</strong> ${
                          candidate.vote_count
                        }</p>
                        <small>Added: ${new Date(
                          candidate.created_at
                        ).toLocaleString()}</small>
                    `;
            candidatesList.appendChild(candidateDiv);
          });
        }
        logResponse(`Retrieved ${result.data.length} candidates`, "success");
      } else {
        logResponse(`Error: ${result.message}`, "error");
      }
    });

  // Get Results
  document
    .getElementById("getResults")
    .addEventListener("click", async function () {
      const result = await apiCall("/get-results");
      const resultsDisplay = document.getElementById("resultsDisplay");

      if (result.status === "success") {
        resultsDisplay.innerHTML = "";

        if (result.results.length === 0) {
          resultsDisplay.innerHTML = "<p>No votes cast yet</p>";
        } else {
          // Group results by position
          const groupedResults = {};
          result.results.forEach((candidate) => {
            if (!groupedResults[candidate.position]) {
              groupedResults[candidate.position] = [];
            }
            groupedResults[candidate.position].push(candidate);
          });

          // Display results for each position
          Object.keys(groupedResults).forEach((position) => {
            const positionDiv = document.createElement("div");
            positionDiv.innerHTML = `<h3>${position}</h3>`;

            groupedResults[position].forEach((candidate) => {
              const resultDiv = document.createElement("div");
              resultDiv.className = "result-item";
              resultDiv.innerHTML = `
                            <strong>${candidate.name}</strong> (${
                candidate.party || "Independent"
              })
                            <span class="vote-percentage">${
                              candidate.vote_count
                            } votes (${candidate.percentage}%)</span>
                        `;
              positionDiv.appendChild(resultDiv);
            });

            resultsDisplay.appendChild(positionDiv);
          });
        }
        logResponse("Election results retrieved successfully", "success");
      } else {
        logResponse(`Error: ${result.message}`, "error");
      }
    });

  // Get Audit Logs
  document
    .getElementById("getAuditLogs")
    .addEventListener("click", async function () {
      const result = await apiCall("/get-audit-logs");
      const auditLogsList = document.getElementById("auditLogsList");

      if (result.status === "success") {
        auditLogsList.innerHTML = "";

        if (result.data.length === 0) {
          auditLogsList.innerHTML = "<p>No audit logs found</p>";
        } else {
          result.data.forEach((log) => {
            const logDiv = document.createElement("div");
            logDiv.className = "audit-item";
            logDiv.innerHTML = `
                        <strong>[${new Date(
                          log.timestamp
                        ).toLocaleString()}]</strong>
                        <br><strong>Action:</strong> ${log.action}
                        <br><strong>Details:</strong> ${log.details}
                    `;
            auditLogsList.appendChild(logDiv);
          });
        }
        logResponse(
          `Retrieved ${result.data.length} audit log entries`,
          "success"
        );
      } else {
        logResponse(`Error: ${result.message}`, "error");
      }
    });

  // Load candidates dropdown on page load
  loadCandidatesDropdown();

  logResponse("Voting system initialized successfully", "success");
});
