const API_URL = "https://api.tecsrcalc.org";

async function get_prediction() {
    const DPM = document.getElementById("dpm").value;
    const APM = document.getElementById("apm").value;
    const MODEL_SELECTION = document.getElementById("model-select").value;

    const EFISH_CONTAINER = document.getElementById("efish-container");
    const RESULTS_CONTAINER = document.getElementById("result-container");
    const MODEL_CONTAINER = document.getElementById("model-container");
    
    RESULTS_CONTAINER.innerText = "Calculating..."

    try {
        const RESPONSE = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({DPM, APM, MODEL_SELECTION})
        });

        if (!RESPONSE.ok) {
            throw new Error(`Server Error: ${RESPONSE.status}`);
        }

        const DATA = await RESPONSE.json();

        if (DATA.error) {
            RESULTS_CONTAINER.innerText = `Error: ${DATA.error}`;
        } else {
            RESULTS_CONTAINER.innerText = DATA.sr;
            MODEL_CONTAINER.innerText = DATA.model;
            EFISH_CONTAINER.innerText = DATA.app;
        }
    } catch (error) {
        console.error("Calculation Failed:", error);
        RESULTS_CONTAINER.innerText = "Failed to calculate SR!";
        MODEL_CONTAINER.innerText = `Error: ${DATA.error}`
    }
}

async function get_metrics() {
    // This is the index metrics, therefore they will be simple_metrics
    const DATE_CONTAINER = document.getElementById("date-container");

    // Model Usage Metrics
    const LOWER_SR_BOUNDS = document.getElementById("lower-sr-bounds");
    const UPPER_SR_BOUNDS = document.getElementById("upper-sr-bounds");
    
    // Table Elements
    const BEGIN_CONT = document.getElementById("beginner-error");
    const INTER_CONT = document.getElementById("intermediate-error");
    const ADV_CONT = document.getElementById("advanced-error");
    const EXP_CONT = document.getElementById("expert-error");
    const MAST_CONT = document.getElementById("master-error");

    try {
        const RESPONSE = await fetch(`${API_URL}/simple_metrics`);
        const DATA = await RESPONSE.json();

        if (RESPONSE.ok) {
            DATE_CONTAINER.innerText = DATA.date;

            BEGIN_CONT.innerText = `±${DATA.b_err} SR`;
            INTER_CONT.innerText = `±${DATA.i_err} SR`;
            ADV_CONT.innerText = `±${DATA.a_err} SR`;
            EXP_CONT.innerText = `±${DATA.e_err} SR`;
            MAST_CONT.innerText = `±${DATA.m_err} SR`;

            LOWER_SR_BOUNDS.innerText = DATA.lower;
            UPPER_SR_BOUNDS.innerText = DATA.upper;
        } else {
            console.error("Simple Metrics Fetch Failed!", error);
            DATE_CONTAINER.innerText = "Failed to load, try again later!";
        }
    } catch (error) {
        console.error("Simple Metrics Fetch Failed!", error);
        DATE_CONTAINER.innerText = "Failed to load, try again later!";
    }
}

const open_linked_detail = () => {
    const hash = window.location.hash;
    if (hash) {
        const detail = document.querySelector(hash);
        if (detail && detail.tagName === 'DETAILS') {
            detail.open = true;
        }
    }
};

document.addEventListener("DOMContentLoaded", get_metrics);
window.addEventListener('load', open_linked_detail);
window.addEventListener('hashchange', open_linked_detail);