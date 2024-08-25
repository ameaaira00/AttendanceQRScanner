document.addEventListener("DOMContentLoaded", function() {
    const toast = document.getElementById("toast");
    if (toast) {
        toast.classList.add("show");
        setTimeout(() => {
            toast.classList.remove("show");
        }, 3000); // Toast will disappear after 3 seconds
    }
});
