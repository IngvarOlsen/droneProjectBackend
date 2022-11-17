function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function getImagesets() {
  fetch("/get-imageSets", {
    method: "GET"
  }).then((_res) => {
    window.location.href = "/";
  });
}
