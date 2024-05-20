/**
 * Initializes event listeners for click and focus
 * @param element   - element that the event listeners are attached to
 * @param selectionFunction - function that is executed when element is clicked or enter is pressed while focused
 */
function focusHandler(element, selectionFunction) {

    element.addEventListener('click', selectionFunction);
    element.addEventListener('keypress', (ev) => {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            element.click();
        }
    });
}