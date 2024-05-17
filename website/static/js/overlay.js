let elements = document.getElementsByClassName('overlay');
elements = [...elements];

elements.forEach(element => {
   element.parentElement.style.position='relative';
   const overlayContainer = document.createElement('div');
   overlayContainer.classList.add('overlayContainer');
   overlayContainer.appendChild(document.createTextNode(element.dataset.overlay));
   element.insertAdjacentElement('afterend', overlayContainer);
   // console.log({'OVERLAY:': `${overlayContainer} is an overlay on ${element} with ${overlayContainer.textContent}`});
   element.parentElement.addEventListener('mouseenter', () => {
      /*overlayContainer.style.visibility = 'visible';     //For no GSAP dependency, use this approach */
      gsap.to(overlayContainer, {autoAlpha:1, duration:0.2});
   });
   element.parentElement.addEventListener('mouseleave', () => {
      gsap.to(overlayContainer, {autoAlpha:0, duration:0.2});
   });
   element.parentElement.addEventListener('focusin', () => {
      gsap.to(overlayContainer, {autoAlpha:1, duration:0.2});
   });
   element.parentElement.addEventListener('focusout', () => {
      gsap.to(overlayContainer, {autoAlpha:0, duration:0.2});
   });
});
