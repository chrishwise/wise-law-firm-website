class carouselItem{
    element;
    position;
    positionAngle;
    textElement;

    constructor(element, position, positionAngle) {
        this.element = element;
        this.position = position;
        this.positionAngle = positionAngle;
    }

    setTextElement(textElement){
        this.textElement = textElement;
    }
}

class carousel3d{
    carouselRoot;
    textContainer;
    arrayOfItems;
    currentItem;
    nextItem;
    previousItem;
    rotationIncrement;
    radius;

    constructor(rootId, textContainerId, radius, withButtons=true) {
        this.carouselRoot = document.getElementById(rootId);
        this.radius = radius;
        this.carouselRoot.style.transform = `translateZ(-${this.radius}px)`;
        let arrayOfElements = gsap.utils.toArray(this.carouselRoot.children);
        this.rotationIncrement = 360 / (arrayOfElements.length);
        this.arrayOfItems = [];
        let rotationAngle = 0;
        arrayOfElements.forEach((item, index) => {
            let newItem = new carouselItem(item, index, rotationAngle);
            selectionHandler(item, () => this.spinToItem(newItem) );
            // Create the text content for each item
            const descriptionElement = document.createElement('p');
            descriptionElement.innerHTML = newItem.element.dataset.description;
            const headingElement = document.createElement('h4');
            headingElement.innerHTML = newItem.element.dataset.title;
            const textElement = document.createElement('div');
            textElement.append(headingElement, descriptionElement);
            textElement.classList.add('textElement');
            newItem.setTextElement(textElement);
            this.textContainer = document.getElementById(textContainerId);
            this.textContainer.appendChild(textElement);
            this.arrayOfItems.push(newItem);
            // Rotate each item to their proper angle4
            item.style.transform = `rotateY(${rotationAngle}deg) translateZ(${radius}px)`;  // Can do this with GSAP
            rotationAngle += this.rotationIncrement;
        });
        // Set the height of the textContainer to the height of its tallest child
        let heightOfTallestChild = 0;
        [...this.textContainer.children].forEach(textElement => {
            if (textElement.offsetHeight > heightOfTallestChild) {
                heightOfTallestChild = textElement.offsetHeight;
            }
        })
        this.textContainer.style.height = heightOfTallestChild + "px";
        // Set the current item. spinToItem sets previous and next.
        this.currentItem = this.arrayOfItems[0];
        this.spinToItem(this.currentItem);
        // Depending on the withButtons parameter, optionally create buttons
        if (withButtons){this.createButtons();}
    }

    createButtons(){
        const nextButton = document.createElement('button');
        nextButton.addEventListener('click', ()=> this.spinToItem(this.nextItem) );
        nextButton.classList.add('btn');
        nextButton.innerHTML = 'Next';
        const previousButton = document.createElement('button');
        previousButton.addEventListener('click', ()=> this.spinToItem(this.previousItem) );
        previousButton.classList.add('btn');
        previousButton.innerHTML = 'Previous';
        this.carouselRoot.parentElement.insertAdjacentElement('afterend', nextButton);
        this.carouselRoot.parentElement.insertAdjacentElement('afterend', previousButton);
    }

    spinToItem(item){
        let angle = -item.positionAngle;
        gsap.to(this.carouselRoot, {rotationY:angle + '_short', duration:1, ease:'power4.out'});
        gsap.to(this.currentItem.textElement, {autoAlpha:0, overwrite:'auto', xPercent:-100, duration:0.5, ease: 'power4.out'});
        gsap.fromTo(item.textElement, {autoAlpha:0, xPercent:100}, {autoAlpha:1, xPercent: 0, duration: 1, ease: 'power4.out'});

        this.currentItem = item;
        this.nextItem = this.arrayOfItems[(this.currentItem.position + 1) % this.arrayOfItems.length];
        this.previousItem = this.arrayOfItems.slice((this.currentItem.position - 1) % this.arrayOfItems.length)[0];
    }

    updateSize(radius) {
        // Update the carousel width by changing its radius
        this.radius = radius;
        this.carouselRoot.style.transform = `translateZ(-${this.radius}px)`;
        this.arrayOfItems.forEach(item => {
            item.element.style.transform = `rotateY(${item.positionAngle}deg) translateZ(${radius}px)`;  // Can do this with GSAP
        });
        // Update the height of the text container
        let heightOfTallestChild = 0;
        [...this.textContainer.children].forEach(textElement => {
            if (textElement.offsetHeight > heightOfTallestChild) {
                heightOfTallestChild = textElement.offsetHeight;
            }
        })
        this.textContainer.style.height = heightOfTallestChild + "px";
    }
}