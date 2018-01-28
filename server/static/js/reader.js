overlay_data = null;

$(document).ready(function() {
    // If absolute URL from the remote server is provided, configure the CORS
    // header on that server.
    var url = '/pdfs/last.pdf';

    // Disable workers to avoid yet another cross-origin issue (workers need
    // the URL of the script to be loaded, and dynamically loading a cross-origin
    // script does not work).
    // PDFJS.disableWorker = true;

    // The workerSrc property shall be specified.
    PDFJS.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

    // Asynchronous download of PDF
    var loadingTask = PDFJS.getDocument(url);
    loadingTask.promise.then(function(pdf) {
        console.log('PDF loaded');

        // Fetch the first page
        var pageNumber = 1;
        pdf.getPage(pageNumber).then(function(page) {
            console.log('Page loaded');

            var scale = 1.0;
            var viewport = page.getViewport(scale);

            // Prepare canvas using PDF page dimensions
            var canvas = document.getElementById('the-canvas');
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            // Render PDF page into canvas context
            var renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            var renderTask = page.render(renderContext);
            renderTask.then(function () {
                console.log('Page rendered');
                setupOverlay(canvas);
            });

        });
    }, function (reason) {
        // PDF loading error
        console.error(reason);
    });

    function setupOverlay(canvas) {
        var overlay = document.getElementById('content');
        overlay.style.height = canvas.height.toString() + "px";
        overlay.style.width = canvas.width.toString() + "px";
        overlay.style.margin = "10px auto";
        $.ajax({
            type: "GET",
            url: "/overlay_info",
            success: function(result) {
                overlay_data = $.parseJSON(result);
                console.log(overlay_data);
                var box = document.createElement("div");
                box.setAttribute("class", "overlay-box");
                box.style.left = `${overlay_data[0].bbox[0]}px`;
                box.style.bottom = `${overlay_data[0].bbox[1]}px`;
                box.style.width = `${overlay_data[0].bbox[2] - overlay_data[0].bbox[0]}px`;
                box.style.height = `${overlay_data[0].bbox[3] - overlay_data[0].bbox[1]}px`;
                box.setAttribute("data-intro", overlay_data[0].data);
                if(overlay_data[0].bbox[0] < (viewport.width / 2)) {
                    box.setAttribute("data-position", "left");
                }
                else {
                    box.setAttribute("data-position", "right");
                }
                box.setAttribute("data-toggle", "chardinjs");
                //var box_data = document.createElement("div");
                //box_data.setAttribute("class", "overlay-box-data");
                //box_data.innerHTML = overlay_data[0].data;
                //box.appendChild(box_data);
                overlay.appendChild(box);
                $('.overlay-box').on("click", function(ev) {
                    ev.preventDefault();
                    console.log("hey");
                    $('body').chardinJs('toggle');
                });
            },
            error: function(result) {
            }
        });
    }
});
