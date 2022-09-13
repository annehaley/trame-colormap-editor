// Modified from https://www.w3schools.com/howto/howto_js_draggable.asp

export function makeDraggable(
  element: HTMLElement,
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
    let newX = element.offsetLeft - pos1;
    let newY = element.offsetTop - pos2;
    if (bounds.y.length == 2 && newY >= bounds.y[0] && newY <= bounds.y[1]) {
      element.style.top = newY + "px";
      snapPoints.y.forEach((snap) => {
        if (Math.abs(snap - newY) <= 5) newY = snap;
      });
    }
    if (bounds.x.length == 2 && newX >= bounds.x[0] && newX <= bounds.x[1]) {
      snapPoints.x.forEach((snap) => {
        if (Math.abs(snap - newX) <= 5) newX = snap;
      });
      element.style.left = newX + "px";
    }
    callback();
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }

  element.onmousedown = dragMouseDown;
}

export function listenDragSelection(
  element: HTMLElement,
  callback: (startPos: number, endPos: number) => void
) {
  let mousedownLocation: number | undefined = undefined;
  function dragMouseDown(e: MouseEvent) {
    if (
      e.target &&
      !(e.target as HTMLElement).classList.contains("color-square")
    ) {
      mousedownLocation = e.offsetX;
    }
  }

  function dragMouseUp(e: MouseEvent) {
    if (mousedownLocation !== undefined) {
      const lower = Math.min(mousedownLocation, e.offsetX);
      const upper = Math.max(mousedownLocation, e.offsetX);
      callback(lower, upper);
    }
  }

  element.onmousedown = dragMouseDown;
  element.onmouseup = dragMouseUp;
}
