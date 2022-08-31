// Modified from https://www.w3schools.com/howto/howto_js_draggable.asp

export default function makeDraggable(
  elmnt: HTMLElement,
  callback: () => void,
  xBounds = [],
  yBounds = []
) {
  let pos1 = 0,
    pos2 = 0,
    pos3 = 0,
    pos4 = 0;

  function dragMouseDown(e: MouseEvent) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e: MouseEvent) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    const newX = elmnt.offsetLeft - pos1;
    const newY = elmnt.offsetTop - pos2;
    if (yBounds.length == 2 && newY >= yBounds[0] && newY <= yBounds[1]) {
      elmnt.style.top = newY + "px";
    }
    if (xBounds.length == 2 && newX >= xBounds[0] && newX <= xBounds[1]) {
      elmnt.style.left = newX + "px";
    }
    callback();
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }

  elmnt.onmousedown = dragMouseDown;
}
