/**
 * Main JavaScript file for EduFlow-AcademySuite.
 *
 * This file contains custom JavaScript to enhance the user experience, primarily
 * for handling UI patterns like modals that are initiated by HTMX events.
 */
document.addEventListener("DOMContentLoaded", function () {
    // This is the bootstrap modal instance, which will be reused.
    let modalInstance = null;

    // The element that will host the modal content.
    const modalElement = document.getElementById('htmx-modal');

    if (modalElement) {
        // Initialize the Bootstrap modal once.
        modalInstance = new bootstrap.Modal(modalElement, {
            keyboard: false // Do not close with keyboard
        });

        // Listen for HTMX events to populate and show the modal.
        htmx.on(modalElement, 'htmx:beforeSwap', (evt) => {
            // Only respond to successful POST requests that are targeting the modal dialog.
            if (evt.detail.xhr.status === 200 && evt.detail.target.id === "htmx-modal-dialog") {
                modalInstance.show();
            }
        });

        // Listen for HTMX events that signal the form was successfully processed.
        htmx.on(modalElement, 'htmx:afterSwap', (evt) => {
            // A 204 (No Content) response from a form submission indicates success.
            // In this case, we hide the modal. The user list is updated by a separate
            // 'userListChanged' trigger.
            if (evt.detail.xhr.status === 204) {
                modalInstance.hide();
            }
        });

        // Clean up the modal content when it's hidden to avoid stale data.
        modalElement.addEventListener('hidden.bs.modal', function () {
            const modalDialog = document.getElementById('htmx-modal-dialog');
            if(modalDialog) {
                modalDialog.innerHTML = '<div class="modal-content"><div class="modal-body">...</div></div>';
            }
        });
    }

    // Generic listener to show a loading state on any HTMX request.
    // This provides visual feedback to the user.
    htmx.on('htmx:beforeRequest', function(evt) {
        const indicator = htmx.find(evt.detail.elt, '.htmx-indicator');
        if (indicator) {
            indicator.style.display = 'inline-block';
        }
    });

    // Hide the loading state when the request is complete.
    htmx.on('htmx:afterRequest', function(evt) {
        const indicator = htmx.find(evt.detail.elt, '.htmx-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    });
});