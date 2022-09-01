// Modified from https://www.w3schools.com/howto/howto_js_draggable.asp

export function makeDraggable(
  elmnt: HTMLElement,
  callback: () => void,
  bounds = {
    x: [],
    y: [],
  },
  snapPoints = {
    x: [],
    y: [],
  }
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
    let newX = elmnt.offsetLeft - pos1;
    let newY = elmnt.offsetTop - pos2;
    if (bounds.y.length == 2 && newY >= bounds.y[0] && newY <= bounds.y[1]) {
      elmnt.style.top = newY + "px";
      snapPoints.y.forEach((snap) => {
        if (Math.abs(snap - newY) <= 5) newY = snap;
      });
    }
    if (bounds.x.length == 2 && newX >= bounds.x[0] && newX <= bounds.x[1]) {
      snapPoints.x.forEach((snap) => {
        if (Math.abs(snap - newX) <= 5) newX = snap;
      });
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
