const issueInput = document.querySelector("#issue");
const analyzeButton = document.querySelector("#analyze");
const counter = document.querySelector("#counter");
const message = document.querySelector("#message");
const results = document.querySelector("#results");
const emptyState = document.querySelector("#empty-state");
const template = document.querySelector("#results-template");

issueInput.addEventListener("input", () => {
  counter.textContent = `${issueInput.value.length.toLocaleString()} / 8,000`;
});

analyzeButton.addEventListener("click", async () => {
  const issue = issueInput.value.trim();
  message.textContent = "";
  if (issue.length < 15) {
    message.textContent = "Please provide a little more detail about the operational issue.";
    issueInput.focus();
    return;
  }
  analyzeButton.disabled = true;
  analyzeButton.querySelector("span").textContent = "Analyzing…";
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ issue }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to analyze the issue.");
    renderResults(data.analysis);
  } catch (error) {
    message.textContent = error.message;
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.querySelector("span").textContent = "Analyze Issue";
  }
});

function renderResults(analysis) {
  const fragment = template.content.cloneNode(true);
  fragment.querySelectorAll("[data-field]").forEach((element) => {
    const value = analysis[element.dataset.field];
    if (Array.isArray(value)) {
      value.forEach((step) => { const item = document.createElement("li"); item.textContent = step; element.appendChild(item); });
    } else {
      element.textContent = value || "Not specified";
    }
  });
  fragment.querySelectorAll("[data-playbook-field]").forEach((element) => {
    const playbook = analysis.matched_operational_playbook;
    element.textContent = playbook?.[element.dataset.playbookField] || "No matching playbook found";
  });
  const copyButton = fragment.querySelector(".copy-button");
  copyButton.addEventListener("click", async () => {
    await navigator.clipboard.writeText(analysis.draft_official_reply || "");
    copyButton.textContent = "Copied";
    setTimeout(() => { copyButton.textContent = "Copy"; }, 1600);
  });
  results.replaceChildren(fragment);
  emptyState.hidden = true;
  results.hidden = false;
}
