async function fetchLogs() {
    const token = localStorage.getItem("access");

    
    if (!token) {
        alert("Please login first");
        window.location.href = "api/users/login/";
        return [];
    }

    try {
        const res = await fetch("/api/analytics/logs/", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        // 🔹 Unauthorized
        if (res.status === 401) {
            alert("Session expired. Login again.");
            window.location.href = "/login/";
            return [];
        }

        const data = await res.json();

        return data.results;

    } catch (error) {
        console.error("Error fetching logs:", error);
        return [];
    }
}
function populateTable(logs) {
    const table = document.getElementById("logTable");
    table.innerHTML = "";

    logs.forEach(log => {
        table.innerHTML += `
            <tr>
                <td>${log.user || "Anonymous"}</td>
                <td>${log.action}</td>
                <td>${log.status}</td>
                <td>${log.timestamp}</td>
            </tr>
        `;
    });
}

function generateStats(logs) {
    document.getElementById("totalRequests").innerText = logs.length;

    const errors = logs.filter(l => l.status >= 400).length;
    document.getElementById("totalErrors").innerText = errors;

    const endpoints = new Set(logs.map(l => l.action));
    document.getElementById("uniqueEndpoints").innerText = endpoints.size;
}

function generateCharts(logs) {

    const endpointCount = {};
    const statusCount = {};
    const userCount = {};
    const timeCount = {};

    logs.forEach(log => {

        endpointCount[log.action] = (endpointCount[log.action] || 0) + 1;
        statusCount[log.status] = (statusCount[log.status] || 0) + 1;
        userCount[log.user || "anon"] = (userCount[log.user || "anon"] || 0) + 1;

        const date = log.timestamp.split("T")[0];
        timeCount[date] = (timeCount[date] || 0) + 1;
    });

    new Chart(document.getElementById("endpointChart"), {
        type: "bar",
        data: {
            labels: Object.keys(endpointCount),
            datasets: [{ data: Object.values(endpointCount) }]
        }
    });

    new Chart(document.getElementById("statusChart"), {
        type: "pie",
        data: {
            labels: Object.keys(statusCount),
            datasets: [{ data: Object.values(statusCount) }]
        }
    });

    new Chart(document.getElementById("userChart"), {
        type: "bar",
        data: {
            labels: Object.keys(userCount),
            datasets: [{ data: Object.values(userCount) }]
        }
    });

    new Chart(document.getElementById("timeChart"), {
        type: "line",
        data: {
            labels: Object.keys(timeCount),
            datasets: [{
                label: "Requests",
                data: Object.values(timeCount)
            }]
        }
    });
}

async function init() {
    const logs = await fetchLogs();

    populateTable(logs);
    generateStats(logs);
    generateCharts(logs);
}

init();