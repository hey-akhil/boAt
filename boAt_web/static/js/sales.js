document.addEventListener("DOMContentLoaded", function () {
  const videos = document.querySelectorAll(".video-box-card video");

  videos.forEach((video) => {
    // Show first frame
    video.pause();
    video.currentTime = 0.01;

    video.addEventListener("mouseenter", () => {
      video.play();
    });

    video.addEventListener("mouseleave", () => {
      video.pause();  // ⛔ Don't reset to 0
    });
  });
});