// ---- mobile nav toggle ----
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
  navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
}

// ---- scroll progress bar ----
const scanProgress = document.getElementById('scanProgress');
function updateProgress(){
  if (!scanProgress) return;
  const h = document.documentElement;
  const scrolled = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
  scanProgress.style.width = (scrolled || 0) + '%';
}
window.addEventListener('scroll', updateProgress, {passive:true});

// ---- banner + hero parallax (homepage only) ----
const bannerMedia = document.getElementById('bannerMedia');
const heroBg = document.getElementById('heroBg');
function parallax(){
  const y = window.scrollY;
  if (bannerMedia) bannerMedia.style.transform = 'translateY(' + (y * 0.35) + 'px)';
  if (heroBg && y < window.innerHeight * 2.2) {
    heroBg.style.transform = 'translateY(' + (y * 0.15) + 'px)';
  }
}
window.addEventListener('scroll', parallax, {passive:true});

// ---- fade-in on scroll ----
const revealEls = document.querySelectorAll('.reveal');
if (revealEls.length) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      }
    });
  }, {threshold:0.15});
  revealEls.forEach(el => io.observe(el));
}

// ---- contact form (no backend — placeholder confirmation) ----
const contactForm = document.getElementById('contactForm');
const formNote = document.getElementById('formNote');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    formNote.classList.add('show');
    contactForm.reset();
  });
}

// ---- video category filtering (videos page) ----
const filterBtns = document.querySelectorAll('.filter-btn');
const videoCards = document.querySelectorAll('.video-card');
if (filterBtns.length) {
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      videoCards.forEach(card => {
        const show = filter === 'all' || card.dataset.category === filter;
        card.classList.toggle('hidden', !show);
      });
    });
  });
}

// ---- shared validation-popup modal ----
// Any page can call window.showValidationModal(["message one", "message two"])
function buildModal(){
  if (document.getElementById('validationModal')) return;
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.id = 'validationModal';
  overlay.innerHTML = `
    <div class="modal-box">
      <div class="modal-eyebrow">Can't continue yet</div>
      <h3>A few things need fixing</h3>
      <ul id="validationModalList"></ul>
      <button type="button" class="btn btn-gold" id="validationModalClose">Got it</button>
    </div>`;
  document.body.appendChild(overlay);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.classList.remove('open');
  });
  document.getElementById('validationModalClose').addEventListener('click', () => {
    overlay.classList.remove('open');
  });
}
window.showValidationModal = function(messages){
  buildModal();
  const list = document.getElementById('validationModalList');
  list.innerHTML = '';
  messages.forEach(msg => {
    const li = document.createElement('li');
    li.textContent = msg;
    list.appendChild(li);
  });
  document.getElementById('validationModal').classList.add('open');
};

document.addEventListener('DOMContentLoaded', function () {
  const track = document.getElementById('testimonialTrack');
  if (!track) return;

  const PAUSE_MS = 3000;   // how long each card set sits still
  const SHIFT_MS = 700;    // how long the slide animation takes

  function step() {
    const firstCard = track.firstElementChild;
    const cardWidth = firstCard.getBoundingClientRect().width;
    const gap = parseFloat(getComputedStyle(track).gap) || 0;
    const shiftAmount = cardWidth + gap;

    track.style.transition = `transform ${SHIFT_MS}ms ease`;
    track.style.transform = `translateX(${shiftAmount}px)`;

    setTimeout(() => {
      // move the last card to the front, snap back with no transition
      track.insertBefore(track.lastElementChild, track.firstElementChild);
      track.style.transition = 'none';
      track.style.transform = 'translateX(0)';
    }, SHIFT_MS);
  }

  setInterval(step, PAUSE_MS + SHIFT_MS);
});