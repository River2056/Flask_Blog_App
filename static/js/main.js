const deletePost = element => {
    const confirmIfDelete = confirm(`Are you sure you want to delete: ${element.id}?`);
    if(confirmIfDelete) {
        location.href = element.href;
    }
};