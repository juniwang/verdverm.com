var editor = null;
var opts = {};

function initEpicEditor() {
    opts = {
        container: 'epiceditor',
        textarea: null,
        basePath: '/static/css/vendor/epiceditor',
        // clientSideStorage: true,
        // localStorageName: 'epiceditor',
        useNativeFullscreen: true,
        parser: marked,
        file: {
            name: 'epiceditor',
            defaultContent: ''
        },
        theme: {
            base: '/themes/base/epiceditor.css',
            preview: '/themes/preview/github.css',
            editor: '/themes/editor/epic-dark.css'
        },
        button: {
            preview: true,
            fullscreen: false,
            bar: true
        },
        focusOnLoad: false,
        shortcut: {
            modifier: 18,
            fullscreen: 70,
            preview: 80
        },
        autogrow: {
            minHeight: 400,
            scroll: true
        },
        string: {
            togglePreview: 'Toggle Preview Mode',
            toggleEdit: 'Toggle Edit Mode',
            toggleFullscreen: 'Enter Fullscreen'
        }
    }
    editor = new EpicEditor(opts).load();
}

function initPostCompose() {
    // button handler
    $("#post-compose-button").on("click",  handlePostComposeSaveDraft);
   
}

function handlePostComposeSaveDraft(event) {
    console.log("Saving Draft");

    var draft = $("#drafts").val();
    var subject = $("#post-compose-field-title").val();
    var dopost = false;
    if ( $("#dopost").is(':checked') ) {
        dopost = true
    }

    if (draft == null) {
        draft = -1;
    }

    var textContent = editor.exportFile();
    // console.log(textContent);
    var htmlContent = editor.exportFile(null,"html");
    // console.log(htmlContent);

    var csrf = $("#csrf_token").val();
    dosend_post_save_draft(draft, subject, textContent, htmlContent, dopost, csrf);
}

function dosend_post_save_draft(draft, title, textbody, htmlbody, dopost, csrf) {
    var post_query = "/posts/edit";
    post_query += "?drafts=" + encodeURIComponent(draft);
    post_query += "&title=" + encodeURIComponent(title);
    post_query += "&dopost=" + encodeURIComponent(dopost);
    post_query += "&textbody=" + encodeURIComponent(textbody);
    post_query += "&htmlbody=" + encodeURIComponent(htmlbody);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", post_query, true);
    xhr.setRequestHeader('X-CSRF-Token', csrf);


    xhr.onload = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // var results = JSON.parse(xhr.responseText);
                console.log(xhr.responseText);
                
            } else {
                console.error(xhr.statusText);
            }
        }
    };



    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    };
    xhr.send(null);
}
