/**
 * Creates event listeners so that mouse clicks and "Enter" presses trigger the selectionFunction.
 * @param element : HTMLElement
 * @param selectionFunction - executes when the element is clicked or when the element has focus and enter is pressed
 */
function selectionHandler(element, selectionFunction) {

    element.addEventListener('click', selectionFunction);
    element.addEventListener('keypress', (ev) => {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            element.click();
        }
    });
}