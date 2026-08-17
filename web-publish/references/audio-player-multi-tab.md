# Multi-Tab Audio Player

Extends `templates/audio-player.html` to support multiple independent track sets
(e.g. textbook + workbook) selectable via tab buttons.

## When to use

When you have 2+ related but distinct audio collections that belong on the same page
and share the same player controls.

## Changes from the single-set template

### 1. Tab UI in header

Add below the `<h1>`/subtitle in `<header>`:

```html
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('set1')">📖 Set 1</button>
  <button class="tab-btn" onclick="switchTab('set2')">✏️ Set 2</button>
</div>
```

CSS for tabs:
```css
.tabs { display: flex; gap: 0; justify-content: center; }
.tab-btn {
  padding: 8px 28px; border: none; cursor: pointer;
  font-size: 0.9rem; font-weight: 700; color: #94a3b8;
  background: transparent; border-bottom: 3px solid transparent;
  transition: all .2s;
}
.tab-btn.active { color: #3b82f6; border-bottom-color: #3b82f6; }
.tab-btn:hover { color: #cbd5e1; }
```

### 2. Two track containers

```html
<div id="track-list">
  <div class="tab-content active" id="tab-set1"></div>
  <div class="tab-content" id="tab-set2"></div>
</div>
```

```css
.tab-content { display: none; }
.tab-content.active { display: block; }
```

### 3. Two separate track arrays + build function

```js
const set1Tracks = [/* ... */];
const set2Tracks = [/* ... */];
let activeTracks = set1Tracks; // tracks currently displayed
let currentTab = 'set1';

function buildTrackList(tracks, containerId) { /* same logic, but use prefix for IDs */ }

buildTrackList(set1Tracks, 'tab-set1');
buildTrackList(set2Tracks, 'tab-set2');
```

### 4. Tab switch handler

```js
function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', false));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.toggle('active', false));
  // Activate correct button + content (match by text content or data attribute)
  // ...
  if (currentIdx >= 0) {
    activeTracks = tab === 'set1' ? set1Tracks : set2Tracks;
  }
}
```

### 5. Prefixed track item IDs

Each tab's track items need unique IDs to avoid collisions. Use a prefix:
```js
const prefix = containerId === 'tab-set2' ? 's2-' : '';
el.id = prefix + 'track-' + t.idx;
```

## Key pitfall: mute-before-seek

The `skip()` and `seek()` functions MUST mute the audio before changing `currentTime`,
then unmute via `requestAnimationFrame`. Without this, browsers produce an audible
glitch/pop/"gong" when seeking while audio is playing:

```js
function skip(sec) {
  if (currentIdx < 0 || !audio.duration) return;
  audio.muted = true;
  audio.currentTime = Math.max(0, Math.min(audio.duration, audio.currentTime + sec));
  requestAnimationFrame(() => { audio.muted = false; });
  showToast((sec > 0 ? '+' : '') + sec + 's');
}
```

Same pattern applies to `seek()` on the progress bar.
