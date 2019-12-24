const deletePost = element => {
    const confirmIfDelete = confirm(`Are you sure you want to delete post: ${element.id}?`);
    if(confirmIfDelete) {
        element.href = `/delete/${element.id}`
    }
};