// This file was made for the Area of Focus section of Firm Overview. The variable names reflect this. To make
// this file a modular component, it must be refactored with generic names for reusability.

function initializeCardReveal() {
    const aofCards = gsap.utils.toArray('.aof-card');
    const overviewContainer = document.getElementById('aofRight');
    const aofContainer = document.getElementById('aofDetail');
    const aofIcon = document.querySelector('#aofDetail img');
    const aofContent = document.querySelector('#aofDetail .content');
    const contentTitle = document.querySelector('#aofDetail .title');
    const contentDescription = document.querySelector('#aofDetail .description');
    let activeCard;

    aofCards.forEach(aofCard => {
        let hover = gsap.to(aofCard, {scale: 1.1, duration: 0.3, paused: true, ease: 'power3.inOut'});
        aofCard.addEventListener('mouseenter', () => {
            hover.play();
        });
        aofCard.addEventListener('mouseleave', () => {
            hover.reverse();
        });
        aofCard.addEventListener('click', () => {
            selectAof(aofCard);
        })
    });


    function selectAof(aofCard) {
        const aofTitle = aofCard.dataset.title;
        const aofDescription = aofCard.dataset.description;

        contentTitle.innerHTML = aofTitle;
        contentDescription.innerHTML = aofDescription;

        if (activeCard) {
            // In case someone clicks on a card behind an already active modal, close the modal
            return hideModal();
        }
        let onLoad = () => {
            aofContainer.querySelector('.img-container').focus({focusVisible: true});
            // Step 1: aofContainer
            Flip.fit(aofContainer, aofCard, {scale: true, fitChild: aofIcon});
            gsap.set(aofContent, {xPercent: -100});
            const cardState = Flip.getState([aofContainer], {props: 'aspectRatio'});
            // set the final properties and animate
            gsap.set(aofContainer, {clearProps: true});
            gsap.set(aofContainer, {xPercent: -50, yPercent: -50, left: "50%", top: "50%", autoAlpha: 1});  // centers the container
            Flip.from(cardState, {
                duration: 0.7,
                ease: 'power3.inOut',
                scale: true
            });
            // aofContent
            const contentState = Flip.getState(aofContent);
            gsap.set(aofContent, {clearProps: true});
            Flip.from(contentState, {
                duration: 0.7,
                ease: 'power3.out',
                delay: 0.3,
            });
            aofIcon.removeEventListener('load', onLoad);
            document.addEventListener('click', hideModal);
            activeCard = aofCard;
            // THIS DENOTES THE END OF THE SECTION PREVIOUSLY IN ONLOAD
        }
        const icon = aofCard.querySelector('img');
        aofIcon.addEventListener('load', onLoad);
        aofIcon.src = icon.src;
        gsap.set(aofCard, {autoAlpha: 0});  // hides the original card

        gsap.to(aofCards, {
            x: -200, autoAlpha: 0, duration: 0.5, ease: 'expo.out',
            stagger: {
                amount: 0.2,
                from: aofCards.indexOf(aofCard)
            }
        }).kill(aofCard, 'x');      // this prevents the original card from moving
        gsap.to(overviewContainer, {xPercent: 50, autoAlpha: 0, duration: 0.5, ease: 'expo.out'});
    }

    function hideModal() {
        document.removeEventListener('click', hideModal);
        let inactiveCards = [...aofCards];
        inactiveCards.splice(aofCards.indexOf(activeCard), 1);   // inactiveCards doesn't contain activeCard
        const t1 = gsap.timeline({defaults: {ease: 'power3.out'}});
        t1.to(aofContent, {xPercent: -100, duration:0.4})
            .add(Flip.fit(aofContainer, activeCard, {scale: true, fitChild: aofIcon, autoAlpha:0.7, duration:0.5, ease:'power3.out'}))
            .set(aofContainer, {autoAlpha: 0})
            .to(inactiveCards, {x:0, autoAlpha:0.7, duration:0.5}, '-=0.5')
            .set(activeCard, {autoAlpha:0.7})
            .to(overviewContainer, {xPercent:0, autoAlpha: 1, duration:0.5, ease:'power3.out' }, '-=0.5' );
        activeCard = null;

        // re-add the following to the Flip.from(aofContainerState) , onInterrupt: () => t1.kill()
    }
}
