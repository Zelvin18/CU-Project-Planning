const form        = document.getElementById("projectForm");
const resultsDiv  = document.getElementById("results");
const downloadBtn = document.getElementById("downloadBtn");
const fabDownload = document.getElementById("fabDownload");

let lastFormData = null;

// ── Shared download logic ──────────────────────────────────────────
async function triggerDownload(btn) {
    if (!lastFormData) return;
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<span class="spinner"></span>Generating...';
    btn.disabled = true;

    try {
        const res = await fetch("/download-report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(lastFormData),
        });

        if (!res.ok) throw new Error("Failed to generate report.");

        const blob     = await res.blob();
        const url      = URL.createObjectURL(blob);
        const a        = document.createElement("a");
        const filename = res.headers.get("Content-Disposition")
            ?.match(/filename="?([^"]+)"?/)?.[1]
            || "Cavendish_Project_Report.txt";

        a.href     = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
        showToast("Report downloaded.", "success");
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.innerHTML = originalHTML;
        btn.disabled = false;
    }
}

// ── Form Submit ────────────────────────────────────────────────────
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector(".btn-primary");
    submitBtn.innerHTML = '<span class="spinner"></span>Calculating...';
    submitBtn.disabled = true;

    const data = collectFormData();
    lastFormData = data;

    try {
        const res  = await fetch("/estimate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        const json = await res.json();

        if (!json.success) throw new Error(json.error || "Estimation failed.");

        renderResults(json.data);
        downloadBtn.disabled = false;
        // Show mobile FAB
        fabDownload.style.display = "flex";
        showToast("Estimates calculated successfully.", "success");
        resultsDiv.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        submitBtn.innerHTML = "Calculate Estimates";
        submitBtn.disabled = false;
    }
});

// ── Download buttons ───────────────────────────────────────────────
downloadBtn.addEventListener("click", () => triggerDownload(downloadBtn));
fabDownload.addEventListener("click",  () => triggerDownload(fabDownload));

// ── Reset ──────────────────────────────────────────────────────────
form.addEventListener("reset", () => {
    resultsDiv.style.display = "none";
    downloadBtn.disabled = true;
    fabDownload.style.display = "none";
    lastFormData = null;
});

// ── Helpers ────────────────────────────────────────────────────────
function collectFormData() {
    return {
        project_title:   document.getElementById("project_title").value.trim(),
        department:      document.getElementById("department").value.trim(),
        project_manager: document.getElementById("project_manager").value.trim(),
        project_type:    document.getElementById("project_type").value,
        project_size:    document.getElementById("project_size").value,
        complexity:      document.getElementById("complexity").value,
        num_staff:       document.getElementById("num_staff").value,
        hours_per_day:   document.getElementById("hours_per_day").value,
        hourly_rate:     document.getElementById("hourly_rate").value,
    };
}

function renderResults(data) {
    document.getElementById("total_effort").textContent    = data.total_effort_hours.toLocaleString();
    document.getElementById("duration_days").textContent   = data.duration_days.toLocaleString();
    document.getElementById("duration_weeks").textContent  = `${data.duration_weeks} weeks / ${data.duration_months} months`;
    document.getElementById("recommended_staff").textContent = data.recommended_staff;
    document.getElementById("total_budget").textContent    = `UGX ${data.total_budget.toLocaleString("en-UG", { minimumFractionDigits: 0 })}`;

    const tbody = document.getElementById("phaseTableBody");
    tbody.innerHTML = "";

    const phases = data.phase_breakdown;
    let totalHours = 0, totalCost = 0;

    for (const [phase, info] of Object.entries(phases)) {
        totalHours += info.hours;
        totalCost  += info.cost;
        const barWidth = Math.round(info.percentage * 1.2);
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${phase}<span class="phase-bar" style="width:${barWidth}px"></span></td>
            <td>${info.percentage}%</td>
            <td>${info.hours.toLocaleString()}</td>
            <td>${info.days.toLocaleString()}</td>
            <td>UGX ${info.cost.toLocaleString("en-UG", { minimumFractionDigits: 0 })}</td>
        `;
        tbody.appendChild(tr);
    }

    // Totals row
    const totalRow = document.createElement("tr");
    totalRow.innerHTML = `
        <td><strong>TOTAL</strong></td>
        <td><strong>100%</strong></td>
        <td><strong>${totalHours.toLocaleString()}</strong></td>
        <td><strong>${data.duration_days}</strong></td>
        <td><strong>UGX ${totalCost.toLocaleString("en-UG", { minimumFractionDigits: 0 })}</strong></td>
    `;
    tbody.appendChild(totalRow);

    resultsDiv.style.display = "block";
}

function showToast(message, type = "info") {
    const existing = document.querySelector(".toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.4s";
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}
