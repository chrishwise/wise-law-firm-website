/**
* Gets the absolute height of an element: height + padding + borders + vertical margin
* @param {Element | string} el - the element or its id
* @return {number} the absolute height, ceiling integer of float representation
*/
function getAbsoluteHeight(el) {
// Get the DOM Node if you pass in a string
el = (typeof el === 'string') ? document.querySelector(el) : el;

const styles = window.getComputedStyle(el);
const margin = parseFloat(styles['marginTop']) + parseFloat(styles['marginBottom']);
return Math.ceil(el.offsetHeight + margin);
}

/**
* An expanding menu that acts as a dropdown menu. It is composed of a trigger, a triggerLink, and an expandableContainer
*/
class expandingMenu{
    #t1;
    #isOpening;
    #isClosing;
    /**
     * Create an expanding menu
     * @param triggerId - Contains the triggerLink and expandableContainer
     * @param expandableContainerId - Container of the menu items that expands upon hover or focus
     */
    constructor(triggerId, expandableContainerId) {
        this.trigger = document.getElementById(triggerId);
        this.triggerLink = this.trigger.querySelector('.nav-link');
        this.expandableContainer = document.getElementById(expandableContainerId);
        this.containerItems = gsap.utils.toArray(this.expandableContainer.children);
        // Determine container height and create hover animation for containerItems
        let totalHeightOfChildren = 0;
        this.containerItems.forEach(child => {
            totalHeightOfChildren += getAbsoluteHeight(child);
            const hover = gsap.fromTo(child,
                {border: '2px solid transparent', x: 0, backgroundColor: 'transparent'},
                {border: '2px solid #A15A22', duration: 0.2, x: 5, backgroundColor: '#FFFFFF', ease: 'power4.inOut', paused: true});
            child.addEventListener('mouseenter', () => hover.play());
            child.addEventListener('focusin', () => hover.play());
            child.addEventListener('mouseleave', () => hover.reverse());
            child.addEventListener('focusout', () => hover.reverse());
            child.tabIndex = 0;     // Make the container items accessible via tab
        });
        // Initialize animation and attach listeners
        this.#t1 = gsap.timeline({paused: true, defaults: {duration: 0.3, ease: 'power3.out'},
            onComplete: () => {
                this.#isOpening=false;
                gsap.set(this.triggerLink, {backgroundColor: 'whitesmoke', borderRadius: '5 0 0 5'});
            }
        });
        this.#t1.fromTo(this.expandableContainer, {rotationY:-90, transformOrigin:'left 50%', height: totalHeightOfChildren},
            {rotationY:0, height: totalHeightOfChildren, duration:0.4})
            .addLabel('expanded')
            .fromTo(this.containerItems, {autoAlpha:0, x: -20}, {autoAlpha:1, x:0, stagger:0.05}, '-=0.4');
        this.attachListeners();
        this.#isOpening = false;
        this.#isClosing = false;
    }
    expandMenu(){
        if (!this.#isClosing) {
            gsap.set(this.triggerLink, {backgroundColor: 'whitesmoke', borderRadius: '5 0 0 5'});
            this.#isOpening = true;
            this.#t1.play();
        } else{
            // menu is closing, so resume from play head
            this.#isOpening = true;
            this.#isClosing = false;
            this.#t1.tweenFromTo(this.#t1.time(), this.#t1.duration(), {
                onComplete: ()=> {
                    this.#isOpening = false;
                }
            });
        }
    }
    closeMenu() {
        if (!this.#isClosing) {
            this.#isClosing = true;
            gsap.set(this.trigger, {backgroundColor: 'transparent'});
            if (this.#isOpening){
                // Start close animation from the current play head to prevent jumping
                this.#t1.tweenFromTo(this.#t1.time(), 0, {ease: 'power4.out',
                    onComplete: () => {
                        this.#isClosing = false;
                        gsap.set(this.triggerLink, {borderRadius: 5, backgroundColor:'white'});
                    }
                })
            } else {
                // Start close animation from the fully expanded position
                this.#t1.tweenFromTo('expanded', 0, {ease: 'power4.out',
                    onComplete: () => {
                        this.#isClosing = false;
                        gsap.set(this.triggerLink, {borderRadius: 5, backgroundColor:'white'});
                    }
                });
            }
        } else {
            console.log('Menu is already closing');;
        }
    }
    attachListeners(){
        this.triggerLink.addEventListener('mouseenter', () => {
            this.expandMenu();
        });
        this.trigger.addEventListener('mouseleave', () => {
            this.closeMenu();
        });
        this.trigger.addEventListener('focusin', () => {
            this.expandMenu();
        });
        this.trigger.addEventListener('focusout', (ev) => {
            if (!this.trigger.contains(ev.relatedTarget)){
                this.closeMenu();
            }
        });
    }
}

