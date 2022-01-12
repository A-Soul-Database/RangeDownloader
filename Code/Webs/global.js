function dialog(operation){
    /*
        show/hide a dialog
            operation int 
                1: open
                0: close
    */
    operation ===1 ? global_dialog.open() : global_dialog.close()
}
function snackbar(message){
    mdui.snackbar({
        message: message,
        position: 'left-bottom',
    });
}