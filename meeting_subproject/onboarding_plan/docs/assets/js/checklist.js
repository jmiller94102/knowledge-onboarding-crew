(function(){
  function storageKey(){
    // Use page path as namespace so different pages can have their own state
    return 'checklist-state:' + (location.pathname || '/');
  }
  function loadState(){
    try { return JSON.parse(localStorage.getItem(storageKey())||'{}'); } catch(e){ return {}; }
  }
  function saveState(state){
    try { localStorage.setItem(storageKey(), JSON.stringify(state)); } catch(e) {}
  }
  function stableIdForCheckbox(cb, idx){
    // Generate a stable id based on list item text content and index as a fallback
    const li = cb.closest('li');
    const text = (li ? li.innerText : cb.nextElementSibling?.innerText || '').trim().toLowerCase();
    return btoa(unescape(encodeURIComponent(text))).slice(0,24) + ':' + idx;
  }
  function init(){
    const state = loadState();
    const checkboxes = document.querySelectorAll('ul input[type="checkbox"], ol input[type="checkbox"]');
    checkboxes.forEach((cb, idx)=>{
      // Only persist task-list checkboxes rendered by pymdownx.tasklist
      if(!cb.closest('li')) return;
      const id = cb.getAttribute('data-check-id') || stableIdForCheckbox(cb, idx);
      cb.setAttribute('data-check-id', id);
      if(state[id] !== undefined){
        cb.checked = !!state[id];
      }
      cb.addEventListener('change', ()=>{
        const newState = loadState();
        newState[id] = cb.checked;
        saveState(newState);
      });
    });
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
