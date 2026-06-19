function deleteNote(noteId) {
    if (confirm('Are you sure you want to delete this note?'))
        fetch("/delete-note", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': '{{ csrf_token() }}'
            },   
            body: JSON.stringify({ noteId: noteId }),
          }).then((_res) => {
            window.location.href = "/";
          });
}