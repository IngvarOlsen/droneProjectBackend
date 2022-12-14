function saveJob(userId, imageSetId) {
  console.log(JSON.stringify({ userId: userId, imageSetId: imageSetId, status:"render", token:"1234567890" }))
  fetch("/savejob", {
    method: "POST",
    body: JSON.stringify({ userId: userId, imageSetId: imageSetId, status:"render", token:"1234567890" }),
  }).then((_res) => {
    console.log(_res)
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

function deleteJob(userId, jobId) {
  console.log("Delete job for user: " + userId + " and job id: " + jobId)
  fetch("/deletejob", {
    method: "DELETE",
    headers: { "Content-Type": "application/json"},
    body: JSON.stringify({ userId: userId, token:"1234567890", jobId: jobId })
  }).then((_res) => {
    window.location.href = "/jobs";
  });
}

// function deleteNote(noteId) {
//   fetch("/delete-note", {
//     method: "POST",
//     body: JSON.stringify({ noteId: noteId }),
//   }).then((_res) => {
//     window.location.href = "/";
//   });
// }
