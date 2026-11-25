// PlantIQ Web Simulator Logic
const API_BASE = window.location.origin;

let lastEventId = null;
let currentGreeting = "Hello! Welcome back!";

// Speech Synthesis Helper
function speak(text) {
  const voiceEnabled = document.getElementById('toggleVoice').checked;
  if (!voiceEnabled) return;

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel(); // Stop current speech
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.1;
    window.speechSynthesis.speak(utterance);
  }
}

// Update UI Telemetry
function updateUI(status) {
  if (!status) return;

  // Plant Status Pill
  const statusBadge = document.getElementById('statusBadge');
  statusBadge.innerText = status.statusLabel;

  const recBox = document.getElementById('recommendationText');
  recBox.innerText = status.recommendation;

  currentGreeting = status.contextualGreeting;

  // Reading metrics
  if (status.currentReading) {
    const r = status.currentReading;
    
    // Soil
    if (r.soilMoisture !== null) {
      document.getElementById('valMoisture').innerText = `${Math.round(r.soilMoisture)}%`;
      document.getElementById('fillMoisture').style.width = `${Math.min(r.soilMoisture, 100)}%`;
      
      let moistLbl = "41–75% HEALTHY";
      if (r.soilMoisture <= 25) moistLbl = "0–25% VERY DRY 🚨";
      else if (r.soilMoisture <= 40) moistLbl = "26–40% NEEDS WATER 💧";
      else if (r.soilMoisture > 75) moistLbl = "76–100% VERY WET 🌊";
      document.getElementById('lblMoistureStatus').innerText = moistLbl;
    }

    // Temp
    if (r.temperature !== null) {
      document.getElementById('valTemp').innerText = `${r.temperature.toFixed(1)}°C`;
      const tempPercent = Math.min(Math.max((r.temperature / 40) * 100, 0), 100);
      document.getElementById('fillTemp').style.width = `${tempPercent}%`;
    }

    // Humidity
    if (r.humidity !== null) {
      document.getElementById('valHumidity').innerText = `${Math.round(r.humidity)}%`;
      document.getElementById('fillHumidity').style.width = `${Math.min(r.humidity, 100)}%`;
    }

    // Distance
    if (r.distance !== null) {
      document.getElementById('valDistance').innerText = `${Math.round(r.distance)} cm`;
      document.getElementById('fillDistance').style.width = `${Math.min((r.distance / 200) * 100, 100)}%`;
      const distLbl = r.distance <= 100 ? "Person Nearby 👋" : "Clear Area (>100 cm)";
      document.getElementById('lblDistanceStatus').innerText = distLbl;
    }
  }

  // Device status dot
  const isDisconnect = document.getElementById('toggleDisconnect').checked;
  const dot = document.getElementById('deviceDot');
  const dotText = document.getElementById('deviceStatusText');

  if (status.deviceOnline && !isDisconnect) {
    dot.className = "dot";
    dotText.innerText = "ESP32 Online";
  } else {
    dot.className = "dot offline";
    dotText.innerText = "ESP32 Offline";
  }
}

// Fetch Latest Plant Status
async function pollStatus() {
  try {
    const res = await fetch(`${API_BASE}/api/plant/status`);
    if (res.ok) {
      const data = await res.json();
      updateUI(data);
    }
  } catch (err) {
    console.error("Error polling plant status:", err);
  }
}

// Fetch Presence Events
async function pollEvents() {
  try {
    const res = await fetch(`${API_BASE}/api/events/latest?mark_read=true`);
    if (res.ok) {
      const event = await res.json();
      if (event && event.event === "personDetected" && event.id !== lastEventId) {
        lastEventId = event.id;
        
        // Show presence banner
        const banner = document.getElementById('presenceBanner');
        banner.style.display = 'flex';

        // Speak greeting
        speak(event.greetingText || currentGreeting);

        setTimeout(() => {
          banner.style.display = 'none';
        }, 5000);
      }
    }
  } catch (err) {
    console.error("Error polling events:", err);
  }
}

// Simulation Input Controls
async function sendSimulatedTelemetry() {
  const isDisconnect = document.getElementById('toggleDisconnect').checked;
  if (isDisconnect) return;

  const moisture = parseFloat(document.getElementById('sliderMoisture').value);
  const temp = parseFloat(document.getElementById('sliderTemp').value);
  const humidity = parseFloat(document.getElementById('sliderHumidity').value);

  const payload = {
    deviceId: "plantiq-01",
    soilMoisture: moisture,
    soilRaw: Math.round(4095 - (moisture / 100) * 2595),
    temperature: temp,
    humidity: humidity,
    distance: 145.0,
    personDetected: false
  };

  try {
    await fetch(`${API_BASE}/api/sensor-data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    pollStatus();
  } catch (err) {
    console.error("Failed to post simulated telemetry:", err);
  }
}

// Trigger Person Approach Simulation
async function simulateApproach() {
  const moisture = parseFloat(document.getElementById('sliderMoisture').value);
  const temp = parseFloat(document.getElementById('sliderTemp').value);
  const humidity = parseFloat(document.getElementById('sliderHumidity').value);

  const payload = {
    deviceId: "plantiq-01",
    event: "personDetected",
    distance: 42.0
  };

  try {
    await fetch(`${API_BASE}/api/sensor-data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        deviceId: "plantiq-01",
        soilMoisture: moisture,
        temperature: temp,
        humidity: humidity,
        distance: 42.0,
        personDetected: true
      })
    });

    const res = await fetch(`${API_BASE}/api/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const eventData = await res.json();
      lastEventId = eventData.id;

      const banner = document.getElementById('presenceBanner');
      banner.style.display = 'flex';
      speak(eventData.greetingText || currentGreeting);

      setTimeout(() => {
        banner.style.display = 'none';
      }, 5000);
    }
  } catch (err) {
    console.error("Approach simulation failed:", err);
  }
}

// Setup Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnSpeak').addEventListener('click', () => {
    speak(currentGreeting);
  });

  document.getElementById('btnSimulateApproach').addEventListener('click', simulateApproach);

  // Slider change listeners
  const sliderM = document.getElementById('sliderMoisture');
  sliderM.addEventListener('input', (e) => {
    document.getElementById('sliderMoistureVal').innerText = `${e.target.value}%`;
    sendSimulatedTelemetry();
  });

  const sliderT = document.getElementById('sliderTemp');
  sliderT.addEventListener('input', (e) => {
    document.getElementById('sliderTempVal').innerText = `${e.target.value}°C`;
    sendSimulatedTelemetry();
  });

  const sliderH = document.getElementById('sliderHumidity');
  sliderH.addEventListener('input', (e) => {
    document.getElementById('sliderHumidityVal').innerText = `${e.target.value}%`;
    sendSimulatedTelemetry();
  });

  // Polling loops
  setInterval(pollStatus, 3000);
  setInterval(pollEvents, 2000);
  pollStatus();
});
