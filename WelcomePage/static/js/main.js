document.addEventListener("DOMContentLoaded", () => {
  // Animation Observer
  const scrollAnimElements = document.querySelectorAll(
    "[data-animate-on-scroll]",
  );
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting || entry.intersectionRatio > 0) {
          const targetElement = entry.target;
          targetElement.classList.add("animate");
          observer.unobserve(targetElement);
        }
      }
    },
    {
      threshold: 0.15,
    },
  );

  for (let i = 0; i < scrollAnimElements.length; i++) {
    observer.observe(scrollAnimElements[i]);
  }

  // Profile Dropdown Toggle
  const profilePic = document.getElementById("profilePic");
  const profileMenuOverlay = document.getElementById("profileMenuOverlay");
  const OPEN_CLASS = "profile-menu-overlay--open";

  if (profilePic && profileMenuOverlay) {
    const openMenu = () => {
      profileMenuOverlay.classList.add(OPEN_CLASS);
      profileMenuOverlay.setAttribute("aria-hidden", "false");
    };

    const closeMenu = () => {
      profileMenuOverlay.classList.remove(OPEN_CLASS);
      profileMenuOverlay.setAttribute("aria-hidden", "true");
    };

    const isOpen = () => profileMenuOverlay.classList.contains(OPEN_CLASS);

    // Toggle dropdown on profile picture click
    profilePic.addEventListener("click", (event) => {
      event.stopPropagation();
      if (isOpen()) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    // Close dropdown when clicking outside of the panel
    profileMenuOverlay.addEventListener("click", (event) => {
      if (event.target === profileMenuOverlay && isOpen()) {
        closeMenu();
      }
    });

    // Close dropdown on Escape key
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && isOpen()) {
        closeMenu();
      }
    });
  }
});
