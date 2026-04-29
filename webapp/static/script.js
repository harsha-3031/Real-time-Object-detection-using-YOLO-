document.addEventListener("DOMContentLoaded", () => {

  const uploadForm = document.getElementById("uploadForm");
  const recordBtn = document.getElementById("recordBtn");
  const statusMsg = document.getElementById("statusMsg");
  const outputContainer = document.getElementById("outputContainer");
  const outputVideo = document.getElementById("outputVideo");
  const countContainer = document.getElementById("countContainer");

  function displayCounts(counts) {
    countContainer.innerHTML = "<h3>Object Counts</h3>";
    for (const key in counts) {
      countContainer.innerHTML += `<p>${key}: ${counts[key]}</p>`;
    }
  }

  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("videoFile");
    if (!fileInput.files.length) return;

    statusMsg.textContent = "Processing video...";
    outputContainer.style.display = "none";

    const formData = new FormData();
    formData.append("video", fileInput.files[0]);

    const res = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.success) {
      outputVideo.src = data.output_url + "?t=" + new Date().getTime();
      displayCounts(data.counts);
      outputContainer.style.display = "block";
      statusMsg.textContent = "Done!";
    }
  });

  recordBtn.addEventListener("click", async () => {

    statusMsg.textContent = "Recording for 10 seconds...";
    outputContainer.style.display = "none";

    const res = await fetch("/live_record", {
      method: "POST"
    });

    const data = await res.json();

    if (data.success) {
      outputVideo.src = data.output_url + "?t=" + new Date().getTime();
      displayCounts(data.counts);
      outputContainer.style.display = "block";
      statusMsg.textContent = "Live analysis complete!";
    }
  });

});
